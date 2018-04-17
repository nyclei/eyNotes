#!/usr/bin/env python
"""
Usage:
Shut down your registry service to avoid race conditions and possible data loss
and then run the command with an image repo like this:
delete_docker_registry_image.py --image awesomeimage --dry-run
"""

import argparse
import json
import logging
import os
import sys
import shutil
import glob

logger = logging.getLogger(__name__)


def del_empty_dirs(s_dir, top_level):
    """recursively delete empty directories"""
    b_empty = True

    for s_target in os.listdir(s_dir):
        s_path = os.path.join(s_dir, s_target)
        if os.path.isdir(s_path):
            if not del_empty_dirs(s_path, False):
                b_empty = False
        else:
            b_empty = False

    if b_empty:
        logger.debug("Deleting empty directory '%s'", s_dir)
        if not top_level:
            os.rmdir(s_dir)

    return b_empty


def get_layers_from_blob(path):
    """parse json blob and get set of layer digests"""
    try:
        with open(path, "r") as blob:
            data_raw = blob.read()
            data = json.loads(data_raw)
            if data["schemaVersion"] == 1:
                result = set([entry["blobSum"].split(":")[1] for entry in data["fsLayers"]])
            else:
                result = set([entry["digest"].split(":")[1] for entry in data["layers"]])
                if "config" in data:
                    result.add(data["config"]["digest"].split(":")[1])
            return result
    except Exception as error:
        logger.critical("Failed to read layers from blob:%s", error)
        return set()

def get_digest_from_blob(path):
    """parse file and get digest"""
    try:
        with open(path, "r") as blob:
            return blob.read().split(":")[1]
    except Exception as error:
        logger.critical("Failed to read digest from blob:%s", error)
        return ""


def get_links(path, _filter=None):
    """recursively walk `path` and parse every link inside"""
    result = []
    for root, _, files in os.walk(path):
        for each in files:
            if each == "link":
                filepath = os.path.join(root, each)
                if not _filter or _filter in filepath:
                    result.append(get_digest_from_blob(filepath))
    return result


class RegistryCleanerError(Exception):
    pass


class RegistryCleaner(object):
    """Clean registry"""

    def __init__(self, registry_data_dir, dry_run=False):
        self.registry_data_dir = registry_data_dir
        if not os.path.isdir(self.registry_data_dir):
            raise RegistryCleanerError("No repositories directory found inside " \
                                       "REGISTRY_DATA_DIR '{0}'.".
                                       format(self.registry_data_dir))
        self.dry_run = dry_run

    def _delete_layer(self, repo, digest):
        """remove blob directory from filesystem"""
        path = os.path.join(self.registry_data_dir, "repositories", repo, "_layers/sha256", digest)
        logger.info("In method _delete_layer %s", path)
        self._delete_dir(path)

    def _delete_blob(self, digest):
        """remove blob directory from filesystem"""
        path = os.path.join(self.registry_data_dir, "blobs/sha256", digest[0:2], digest)
        logger.info("In method _delete_blob %s", path)
        self._delete_dir(path)

    def _blob_path_for_revision(self, digest):
        """where we can find the blob that contains the json describing this digest"""
        return os.path.join(self.registry_data_dir, "blobs/sha256",
                            digest[0:2], digest, "data")

    def _blob_path_for_revision_is_missing(self, digest):
        """for each revision, there should be a blob describing it"""
        return not os.path.isfile(self._blob_path_for_revision(digest))

    def _get_layers_from_blob(self, digest):
        """get layers from blob by digest"""
        return get_layers_from_blob(self._blob_path_for_revision(digest))

    def _delete_dir(self, path):
        """remove directory from filesystem"""
        logger.info("In method _delete_dir %s", path)
        if self.dry_run:
            logger.info("DRY_RUN: would have deleted %s", path)
        else:
            logger.info("Deleting %s", path)
            try:
                shutil.rmtree(path)
                #self._delete_dir(path)

            except Exception as error:
                logger.critical("Failed to delete directory:%s", error)

    def _delete_from_tag_index_for_revision(self, repo, digest):
        """delete revision from tag indexes"""
        paths = glob.glob(
            os.path.join(self.registry_data_dir, "repositories", repo,
                         "_manifests/tags/*/index/sha256", digest)
        )
        for path in paths:
            self._delete_dir(path)

    def _delete_revisions(self, repo, revisions, blobs_to_keep=None):
        """delete revisions from list of directories"""
        if blobs_to_keep is None:
            blobs_to_keep = []
        for revision_dir in revisions:
            digests = get_links(revision_dir)
            for digest in digests:
                self._delete_from_tag_index_for_revision(repo, digest)
                if digest not in blobs_to_keep:
                    self._delete_blob(digest)

            self._delete_dir(revision_dir)

    def _get_tags(self, repo):
        """get all tags for given repository"""
        path = os.path.join(self.registry_data_dir, "repositories", repo, "_manifests/tags")
        if not os.path.isdir(path):
            logger.critical("No repository '%s' found in repositories directory %s",
                             repo, self.registry_data_dir)
            return None
        result = []
        for each in os.listdir(path):
            filepath = os.path.join(path, each)
            if os.path.isdir(filepath):
                result.append(each)
        return result

    def _get_repositories(self):
        """get all repository repos"""
        result = []
        root = os.path.join(self.registry_data_dir, "repositories")
        for each in os.listdir(root):
            filepath = os.path.join(root, each)
            if os.path.isdir(filepath):
                inside = os.listdir(filepath)
                if "_layers" in inside:
                    result.append(each)
                else:
                    for inner in inside:
                        result.append(os.path.join(each, inner))
        return result

    def _get_all_links(self, except_repo=""):
        """get links for every repository"""
        result = []
        repositories = self._get_repositories()
        for repo in [r for r in repositories if r != except_repo]:
            path = os.path.join(self.registry_data_dir, "repositories", repo)
            for link in get_links(path):
                result.append(link)
        return result

    def prune(self):
        """delete all empty directories in registry_data_dir"""
        del_empty_dirs(self.registry_data_dir, True)

    def _layer_in_same_repo(self, repo, tag, layer):
        """check if layer is found in other tags of same repository"""
        for other_tag in [t for t in self._get_tags(repo) if t != tag]:
            path = os.path.join(self.registry_data_dir, "repositories", repo,
                                "_manifests/tags", other_tag, "current/link")
            manifest = get_digest_from_blob(path)
            try:
                layers = self._get_layers_from_blob(manifest)
                if layer in layers:
                    return True
            except IOError:
                if self._blob_path_for_revision_is_missing(manifest):
                    logger.warn("Blob for digest %s does not exist. Deleting tag manifest: %s", manifest, other_tag)
                    tag_dir = os.path.join(self.registry_data_dir, "repositories", repo,
                                           "_manifests/tags", other_tag)
                    self._delete_dir(tag_dir)
                else:
                    raise
        return False

    def _manifest_in_same_repo(self, repo, tag, manifest):
        """check if manifest is found in other tags of same repository"""
        for other_tag in [t for t in self._get_tags(repo) if t != tag]:
            path = os.path.join(self.registry_data_dir, "repositories", repo,
                                "_manifests/tags", other_tag, "current/link")
            other_manifest = get_digest_from_blob(path)
            if other_manifest == manifest:
                return True

        return False

    def delete_entire_repository(self, repo):
        """delete all blobs for given repository repo"""
        logger.debug("Deleting entire repository '%s'", repo)
        repo_dir = os.path.join(self.registry_data_dir, "repositories", repo)
        if not os.path.isdir(repo_dir):
            raise RegistryCleanerError("No repository '{0}' found in repositories "
                                       "directory {1}/repositories".
                                       format(repo, self.registry_data_dir))
        links = set(get_links(repo_dir))
        all_links_but_current = set(self._get_all_links(except_repo=repo))
        for layer in links:
            if layer in all_links_but_current:
                logger.debug("Blob found in another repository. Not deleting: %s", layer)
            else:
                self._delete_blob(layer)
        self._delete_dir(repo_dir)

    def delete_repository_tag(self, repo, tag):
        """delete all blobs only for given tag of repository"""
        logger.debug("Deleting repository '%s' with tag '%s'", repo, tag)
        tag_dir = os.path.join(self.registry_data_dir, "repositories", repo, "_manifests/tags", tag)
        if not os.path.isdir(tag_dir):
            raise RegistryCleanerError("No repository '{0}' tag '{1}' found in repositories "
                                       "directory {2}/repositories".
                                       format(repo, tag, self.registry_data_dir))
        manifests_for_tag = set(get_links(tag_dir))
        revisions_to_delete = []
        blobs_to_keep = []
        layers = []
        all_links_not_in_current_repo = set(self._get_all_links(except_repo=repo))
        for manifest in manifests_for_tag:
            logger.debug("Looking up filesystem layers for manifest digest %s", manifest)

            if self._manifest_in_same_repo(repo, tag, manifest):
                logger.debug("Not deleting since we found another tag using manifest: %s", manifest)
                continue
            else:
                revisions_to_delete.append(
                    os.path.join(self.registry_data_dir, "repositories", repo,
                                 "_manifests/revisions/sha256", manifest)
                )
                if manifest in all_links_not_in_current_repo:
                    logger.debug("Not deleting the blob data since we found another repo using manifest: %s", manifest)
                    blobs_to_keep.append(manifest)

                layers.extend(self._get_layers_from_blob(manifest))

        layers_uniq = set(layers)
        for layer in layers_uniq:
            if self._layer_in_same_repo(repo, tag, layer):
                logger.debug("Not deleting since we found another tag using digest: %s", layer)
                continue

            self._delete_layer(repo, layer)
            if layer in all_links_not_in_current_repo:
                logger.debug("Blob found in another repository. Not deleting: %s", layer)
            else:
                self._delete_blob(layer)

        self._delete_revisions(repo, revisions_to_delete, blobs_to_keep)
        self._delete_dir(tag_dir)

    def delete_untagged(self, repo):
        """delete all untagged data from repo"""
        logger.debug("Deleting utagged data from repository '%s'", repo)
        repositories_dir = os.path.join(self.registry_data_dir, "repositories")
        repo_dir = os.path.join(repositories_dir, repo)
        if not os.path.isdir(repo_dir):
            raise RegistryCleanerError("No repository '{0}' found in repositories "
                                       "directory {1}/repositories".
                                       format(repo, self.registry_data_dir))
        tagged_links = set(get_links(repositories_dir, _filter="current"))
        layers_to_protect = []
        for link in tagged_links:
            layers_to_protect.extend(self._get_layers_from_blob(link))

        unique_layers_to_protect = set(layers_to_protect)
        for layer in unique_layers_to_protect:
            logger.debug("layer_to_protect: %s", layer)

        tagged_revisions = set(get_links(repo_dir, _filter="current"))

        revisions_to_delete = []
        layers_to_delete = []

        dir_for_revisions = os.path.join(repo_dir, "_manifests/revisions/sha256")
        for rev in os.listdir(dir_for_revisions):
            if rev not in tagged_revisions:
                revisions_to_delete.append(os.path.join(dir_for_revisions, rev))
                for layer in self._get_layers_from_blob(rev):
                    if layer not in unique_layers_to_protect:
                        layers_to_delete.append(layer)

        unique_layers_to_delete = set(layers_to_delete)

        self._delete_revisions(repo, revisions_to_delete)
        for layer in unique_layers_to_delete:
            self._delete_blob(layer)
            self._delete_layer(repo, layer)


    def get_tag_count(self, repo):
        logger.debug("Get tag count of repository '%s'", repo)
        repo_dir = os.path.join(self.registry_data_dir, "repositories", repo)
        tags_dir = os.path.join(repo_dir, "_manifests/tags")

        if os.path.isdir(tags_dir):
            tags = os.listdir(tags_dir)
            return len(tags)
        else:
            logger.info("Tags directory does not exist: '%s'", tags_dir)
            return -1
    
    def get_digests_only_from_blob(self,path):
        """parse json blob and get set of layer digests, layers only, no config"""
        try:
            with open(path, "r") as blob:
                data_raw = blob.read()
                data = json.loads(data_raw)
                if data["schemaVersion"] == 2:
                    result = set([entry["digest"].split(":")[1] for entry in data["layers"]])
                    if "config" in data:
                        result.add(data["config"]["digest"].split(":")[1])
                return result
        except Exception:
            """ Either blob data is binary or unable to read   """
            #logger.info("Either blob data is binary or unable to read")
            return set()


    def find_orphan_layers(self):
        """find all layer directories  exist the registry"""
        all_repositories = self._get_repositories()
        all_layers_dir =[]
        layers_to_full_path = {}
        for repo in all_repositories:
            layer_path_root = os.path.join(self.registry_data_dir, "repositories", repo,
                                    "_layers/sha256/")
            for root, dirs, files in os.walk(layer_path_root): 
                for filename in files:
                    fullpath = os.path.join(root, filename)
                    layer = get_digest_from_blob(fullpath)
                    layers_to_full_path[layer] = fullpath
                    all_layers_dir.append(layer)
        
        print "All layer directories in the registry :" 
        for a in all_layers_dir:
            print a
        
        """ find all blob directories exist the registry"""
        all_blobs_dir =[]
        blobs_path_root = os.path.join(self.registry_data_dir, "blobs/sha256/")
        subdir = os.listdir(blobs_path_root)
        for s in subdir:
            blubs = os.listdir(os.path.join( blobs_path_root,s))
            for aBlub in blubs:
                all_blobs_dir.append(aBlub)

        print "All blob directories in the registry:"       
        for b in all_blobs_dir:
            print(b)

        """ find all digests that layers/configs of the blobs reference to """
        layers_used_in_blobs = []
        blob_root = os.path.join(self.registry_data_dir, "blobs/sha256/")
        for root, dirs, files in os.walk(blob_root): 
            for aFilename in files:
                blobpath = os.path.join(root, aFilename)

                temp_set = self.get_digests_only_from_blob(blobpath)
                for element_in_set in temp_set:
                    layers_used_in_blobs.append(element_in_set)

        print "All layers/configs that blobs reference to:"        
        for aDigest in layers_used_in_blobs:
                    print(aDigest)
        
        """Search for Orphan Layers""" 
        orphan_layers_found = []
        orphan_blobs_found = []
        for each_layer in all_layers_dir:
            if each_layer not in all_blobs_dir:
                logger.info(each_layer)
                logger.info("is an orphan layer that points to a blob directory that no longer exists. ")
                orphan_layers_found.append(each_layer)
            
            if each_layer not in layers_used_in_blobs:
                logger.info(each_layer)
                logger.info("is an orphan layer that is not referenced by any blob digests. ") 
                orphan_layers_found.append(each_layer)
                if each_layer in  all_blobs_dir:
                     logger.info("and its correspondent blob storage is an orphan blob. ")  
                     orphan_blobs_found.append(each_layer)
        
        """Delete for Orphan Layers/Blobs"""
        if not orphan_layers_found:
            logger.info("No Orphan Layers/Blobs Found.")  
        else:
            for orphan_layer in orphan_layers_found:
                _delete_dir(layers_to_full_path[orphan_layer])
            for orphan_blob  in orphan_blobs_found:
                _delete_dir(layers_to_full_path[orphan_blob])


def main():
    """cli entrypoint"""
    parser = argparse.ArgumentParser(description="Cleanup docker registry")
    parser.add_argument("-i", "--image",
                        dest="image",
                        required=False,
                        help="Docker image to cleanup")
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="verbose")
    parser.add_argument("-n", "--dry-run",
                        dest="dry_run",
                        action="store_true",
                        help="Dry run")
    parser.add_argument("-f", "--force",
                        dest="force",
                        action="store_true",
                        help="Force delete (deprecated)")
    parser.add_argument("-p", "--prune",
                        dest="prune",
                        action="store_true",
                        help="Prune")
    parser.add_argument("-o", "--orphan",
                        dest="orphan",
                        action="store_true",
                        help="Orphan")
    parser.add_argument("-u", "--untagged",
                        dest="untagged",
                        action="store_true",
                        help="Delete all untagged blobs for image")
    args = parser.parse_args()


    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s'))
    logger.addHandler(handler)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    # make sure not to log before logging is setup. that'll hose your logging config.
    if args.force:
        logger.info(
            "You supplied the force switch, which is deprecated. It has no effect now, and the script defaults to doing what used to be only happen when force was true")
    if args.image:
        splitted = args.image.split(":")
        if len(splitted) == 2:
            image = splitted[0]
            tag = splitted[1]
        else:
            image = args.image
            tag = None

    if 'REGISTRY_DATA_DIR' in os.environ:
        registry_data_dir = os.environ['REGISTRY_DATA_DIR']
    else:
        registry_data_dir = "/opt/registry_data/docker/registry/v2"

    try:
        cleaner = RegistryCleaner(registry_data_dir, dry_run=args.dry_run)
        if args.untagged:
            cleaner.delete_untagged(image)
        elif args.orphan:
            cleaner.find_orphan_layers()
        else:
            if tag:
                tag_count = cleaner.get_tag_count(image)
                if tag_count == 1:
                    cleaner.delete_entire_repository(image)
                else:
                    cleaner.delete_repository_tag(image, tag)
            else:
                cleaner.delete_entire_repository(image)

        if args.prune:
            cleaner.prune()
            
    except RegistryCleanerError as error:
        logger.fatal(error)
        sys.exit(1)


if __name__ == "__main__":
    main()


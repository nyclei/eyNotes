package com.adobe.example;
 
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Service;
import org.apache.felix.scr.annotations.Property;
 
import org.apache.sling.api.SlingHttpServletRequest;
import org.apache.sling.api.SlingHttpServletResponse;
import org.apache.sling.api.servlets.SlingSafeMethodsServlet;
 
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
 
import org.apache.commons.httpclient.*;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
 
@Component(metatype=true)
@Service
public class Flushcache extends SlingSafeMethodsServlet {
 
    @Property(value="/bin/flushcache")
    static final String SERVLET_PATH="sling.servlet.paths";
 
    private Logger logger = LoggerFactory.getLogger(this.getClass());
 
    public void doGet(SlingHttpServletRequest request, SlingHttpServletResponse response) {
        try{ 
            //retrieve the request parameters
            String handle = request.getParameter("handle");
            String page = request.getParameter("page");
 
            //hard-coding connection properties is a bad practice, but is done here to simplify the example
            String server = "localhost"; 
            String uri = "/dispatcher/invalidate.cache";
 
            HttpClient client = new HttpClient();
 
            PostMethod post = new PostMethod("http://"+host+uri);
            post.setRequestHeader("CQ-Action", "Activate");
            post.setRequestHeader("CQ-Handle",handle);
             
            StringRequestEntity body = new StringRequestEntity(page,null,null);
            post.setRequestEntity(body);
            post.setRequestHeader("Content-length", String.valueOf(body.getContentLength()));
            client.executeMethod(post);
            post.releaseConnection();
            //log the results
            logger.info("result: " + post.getResponseBodyAsString());
            }
        }catch(Exception e){
            logger.error("Flushcache servlet exception: " + e.getMessage());
        }
    }
}


#### used maven? which file contains maven configurations?
pom.xml

#### How to add a external package (jar) in maven project?
Add it as a <dependency> element.

#### What is the difference between Set and Map?

Set contains values only whereas Map contains key and values both.

#### What is the difference between HashSet and HashMap?

HashSet contains only values whereas HashMap contains entry(key,value). HashSet can be iterated but HashMap need to convert into Set to be iterated

#### What is the difference between HashMap and Hashtable

HashMap is not synchronized.	Hashtable is synchronized.
HashMap can contain one null key and multiple null values.	Hashtable cannot contain any null key or null value.

#### What does the hashCode() method?

The hashCode() method returns a hash code value (an integer number).

The hashCode() method returns the same integer number, if two keys (by calling equals() method) are same.

But, it is possible that two hash code numbers can have different or same keys.


#### Why we override equals() method?

The equals method is used to check whether two objects are same or not. It needs to be overridden if we want to check the objects based on property.

#### 'final' method means?
 method can't be overridden

#### 'final' variable means?
final fields must be initialized

#### What is thread?

A thread is a lightweight subprocess.
It is a separate path of execution.It is called separate path of execution because each thread runs in a separate stack frame.


#### How to implement a thread class in Java?
implements Runnable class, extends Thread class

#### How to lock a java *method* among multiple threads?.. say avoiding race condition... or say make a *method* mutual exclusive?

#### How to lock a *block of java code*.. say avoiding race condition... or say make a block of code mutual exclusive?

#### what is the method you must implments in a Thread class?
run()

#### How to invoke a thread instance?
calling start()

#### What's difference between run() and start()?

#### What is a deadlock? give me an example
2 or 3 threads:
   a is waiting for resource used by b,
   b is waiting for resource used by c,
   c is waiting for resource used by a


#### What is serialization?

Serialization is a process of writing the state of an object into a byte stream. (for I/O)


#### diff 'static' variable vs. non-static variable
One is class variable, accessible by any instance
one is instance variable, accessible by 'this' only

#### diff static method vs non-static method
One is class method, accessible by any instance.
One is instance method, accessible by 'this' only

#### What's the difference among private, public, protected ?

#### Java natively supports multi-inheritance?
No

#### If NO, is there anyway to make Java support multi-inheritance?
Using Interface

#### Could you tell me the difference between abstract class and interface?
Abstract class has limited implementation/mothod body,
allows some fields and constants, can have constructor

Interface defines method without any implementation,
no fields allowed, no constructor

#### how to control the Exception?
If
- using try-catch block
- using throws in method declaration to throw it out.


#### What is runtime exception? do we have to try-catch it?
RuntimeException and its subclasses are unchecked exceptions. Unchecked exceptions do not need to be declared in a method or constructor's throws clause if they can be thrown by the execution of the method or constructor and propagate outside the method or constructor boundary.

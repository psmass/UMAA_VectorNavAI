
![](https://github.com/psmass/DDSexamples/blob/master/RtiAsOne.png)


*** THIS DIRECTORY CONTAINS: ***
UMAA GlobalPos/SpeedStatus Service Provider and Consumer Example using RTI's AI Connext Chatbot.

AI accelerates your development and allows you to focus on the problem space, and compsci expertise (data structs, algorithms, OS concepts, OO Concepts) vs. language and API detail. 
With AI, you are the Captain, AI is the copilot. It gets about 92-99% correct, leaving you to figure out whats wrong.

The general approach of this example, is to use VS Code to create the XML from the block diagram (drawing). Then use RTI's System Designer to creat the code from the XML.
System Designer provides a predictable "template" to create the code and will use XML Application creation, Dynamic Data Types, and Waitsets. Normally with a large Data model such as UMAA, using Dynamic Types is less desirable because you lose Intelisense to set nested fields. However, with AI you can now have the Connext Bot provide you the code to set these highly nested fields. Advantages of Dynamic Types over Compiled types include, data samples and of all 'Dynamic Type' (I.e., not type specific) allowing non-templatized base class to be used (run time performance of Dynamic types is slightly higher, but minimal). 

** NOTE: Uses RTI Connext 7.5 EAR ** UMAA Distro A - 6.0 (as can be found on the AUVSI website)
REQUIRES and RTI License to use Connext. Get a free license (and access to RTI's very extensive documentation and ConnextBot -as well as other resources), visit www.rti.com.

The only files required are the VectorNavBlockDiagram, and the UMAA IDL in the data_model directory.
(The drawing could be a pic of hand drawn white board drawing. Best Practice to put the topics with the arrows of Readers and Writers. Because we wanted AI to use the existing data-model vs creating its own, I was very explicit about the topic names and where they could be found. You want to @connext /IncludeWorkspace directive.

Everything else can be removed to rebuild the apps using Connext Chatbot with Visual Studio Code (RTI Connext Chatbot VS Code plugin and RTI's System Designer.

The chatbot provided the script/RTI code gen command to create XML equivalent of the all the IDL files, stored in the same directory (e.g. UMAA::CO::CommsChannelMessageConfigType.idl and .xml.)

Step0: Bring the project up in VS Code (you may use the existing UMAA_VN.code-workspace files or create your own.

Step1: Create XML equivalent of IDL using RTI's CodGen
(prior, I had AI generate the script found in the /scripts folder to make all the include files relative in the idl)

Step2: In VS Code, make sure you have rti Connext DDS 7.5 installed and active @connext /showConnextInstallations @connext  /setConnextInstallation

Step3: In VS code,  @connext /includeWorkspace (includes all files in the workspace. (note - it complains about too many files, but no adverse effects.

Step4: In VS Code,  @connext /generateSystemXmlModel (this should generate an XML file with the What (topics), How (QoS), and Who (Participants, Readers, writers). Include are both participants HSMSTControlParticipant (Service Consumer) and the VectorNavParticipant (Service Provider) as well as registering topics and all data types used. Check the QoS you like, for me it generated what I wanted, writer writing strict reliable and reader reading best effort (you can change these defaults or what it generates in the next step (System Designer) 

Step5: @connext /startSystemDesigner Pull the generated XML file into System Designer - create a project import the xml (note we have one already called VectorNavSystem.rtisdproj, but again, you can create your own or use the one provided. Modify any QoS you would like.

Step6: In System Designer, Select each participant, Rightclick and select Generate code. Select use Wait-sets and Python (or what language you like).

Step7: in VS Code, ask AI to modify any business logic - e.g. @connext  in the while True loop, make the the SpeedThroughAir start from 100 incrementing by an increment of 10 to 400, and then by reversing the increment back to 100 . Have this pattern repeat indefinitely

Run each Provider and Consumer application

Note: In the folder py/VecNav_ex are versions of the apps created only with VS Code (Much less predictable) and more back and forth with the Connext Chatbot to get things 'right'.




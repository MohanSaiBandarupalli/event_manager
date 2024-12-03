### Homework 10 : Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

### The following issues were resolved as part of this project:

1. [SMTP Error](https://github.com/MohanSaiBandarupalli/event_manager/issues/11)  
2. [Token Errors](https://github.com/MohanSaiBandarupalli/event_manager/issues/9)  
3. [Validation for Email](https://github.com/MohanSaiBandarupalli/event_manager/issues/7)  
4. [URL Validation](https://github.com/MohanSaiBandarupalli/event_manager/issues/5)  
5. [Login Request](https://github.com/MohanSaiBandarupalli/event_manager/issues/4)  
6. [Username Validation](https://github.com/MohanSaiBandarupalli/event_manager/issues/2)


### Issue Descriptions

1. **Username Validation**  
   Ensured that usernames meet specific criteria, such as uniqueness and format compliance. This involved implementing checks for special characters, length restrictions, and duplicates during user creation.

2. **Password Validation**  
   Strengthened password security by enforcing rules such as minimum length, complexity (special characters, numbers, uppercase), and rejection of common patterns, enhancing user account safety.

3. **URL Validation**  
   Added validation logic to ensure that user-provided URLs (e.g., profile links) adhere to standard URL formats and avoid invalid entries that could disrupt workflows.

4. **Email Validation**  
   Implemented robust email validation to ensure correctness, including verifying domain formats and handling edge cases like unsupported characters or incomplete email addresses.

5. **Token Errors**  
   Resolved issues with authentication tokens, including handling expired tokens, malformed tokens, and improving error messages to provide clarity during user authentication processes.

6. **SMTP Error**  
   Debugged and fixed issues with the SMTP server configuration, ensuring secure email communication for operations like verification and notifications. This involved handling connection errors and upgrading email limits.


### Pytest Coverage
![Test Coverage](https://github.com/user-attachments/assets/73c727db-6654-4c88-9f2c-9536fa067251)

![Test Coverage](https://github.com/user-attachments/assets/9b430145-d223-4542-972f-a77af3d2e203)

![docker Repository ](https://github.com/user-attachments/assets/7bd8e5ec-ac43-42d1-a251-198f7c127f37)

![Image Deployed in Docker](https://github.com/user-attachments/assets/10aadbf3-0ddb-4633-a6f5-e19e60c85940)



### Overall Learnings and Challenges Faced

This project provided an in-depth understanding of developing and maintaining a robust event management system while adhering to best practices in software development. The primary focus areas included implementing strong validation mechanisms, integrating secure communication channels, and ensuring comprehensive test coverage for all critical functionalities. Each issue presented unique learning opportunities that enhanced not only the technical implementation but also problem-solving and debugging skills.

Throughout the project, several challenges were encountered, such as resolving validation inconsistencies, handling token and email errors, and configuring the SMTP server for reliable email delivery. For example, the **SMTP Error** required a deep dive into secure email configurations and debugging server-side connections. Similarly, the **Token Errors** involved understanding and resolving edge cases like expired and malformed tokens, which highlighted the importance of designing resilient systems. The iterative process of identifying root causes, implementing fixes, and writing exhaustive test cases significantly strengthened the quality and reliability of the system.

The experience emphasized the importance of version control, collaborative issue tracking, and continuous integration for modern development. By actively managing issues such as **Username Validation** and **Password Validation**, the project demonstrated how thoughtful design and comprehensive testing can eliminate bugs early and create a seamless user experience. This project not only enhanced technical expertise in areas like validation, security, and CI/CD pipelines but also underscored the value of meticulous documentation of successfully delivering software solutions.

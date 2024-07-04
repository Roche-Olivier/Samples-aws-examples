## About "Assume_role"

- This part is how to assume a role on anohter system.
- Assuming a role on AWS gives you back the access_key, secret_key, and token.
- [Here](https://github.com/Roche-Olivier/aws-examples/blob/main/Python/Assume_role/Assume-role.py) is an example of just assuming a role and getting those values back.

### More details - How do i handle a AWS client creation ?
- To be able to instantiate an AWS client item you can crreate a session with the assumed role
- To be able to create a session for the role you have assumed you need the previous values, so we will chain the calls to the methods.
- This session expiry time is pre-determined by the provider.
- [This](https://github.com/Roche-Olivier/aws-examples/blob/main/Python/Assume_role/Assume-role_Session.py) is an example of creating a session from the assumed role.

### What can i then do with the session
- The session can then be used to call AWS clients for example S3.
- On the client you can then execute specific actions
- [Link](https://github.com/Roche-Olivier/aws-examples/blob/main/Python/Assume_role/Assume-role_Session_S3.py) to the complete example of assuming a role creating a new session and performing an action on the session.

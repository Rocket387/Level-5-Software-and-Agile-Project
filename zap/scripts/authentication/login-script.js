function authenticate(helper, paramsValues, credentials) {
    var req = new org.parosproxy.paros.network.HttpRequestHeader();
    req.setURI(new org.apache.commons.httpclient.URI("http://notekeeper:8080/api/auth/login", false));
    req.setMethod("POST");
    req.setHeader("Content-Type", "application/json");

    var body = JSON.stringify({
        email: credentials.getParam("email"),  
        password: credentials.getParam("password")
    });

    var msg = helper.prepareMessage();
    msg.setRequestHeader(req);
    msg.setRequestBody(body);
    helper.sendAndReceive(msg);

    return true;
}

function getRequiredParamsNames() {
    return ["email", "password"]; 
}

function getOptionalParamsNames() {
    return [];
}

function getCredentialsParamsNames() {
    return ["email", "password"]; 
}

var UserProfile = (function() {
  var full_name = "";

  var getName = function() {
    return full_name;    // Or pull this from cookie/localStorage
  };

  var getSessionId = function() {
    return localStorage.getItem('sessionId')
  }

  var setName = function(name, sessionId) {
    full_name = name;     
    localStorage.setItem('user_name', full_name);
    localStorage.setItem('sessionId', sessionId);
  };

  return {
    getName: getName,
    setName: setName,
    getSessionId: getSessionId
  }

})();

export default UserProfile;
export function isLoggedIn() {
  return localStorage.getItem("access_token")!==null && localStorage.getItem("access_token")!=="undefined";
}

export function deleteTokens(){
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
}

export function getUserName() {
  return localStorage.getItem("username")
}

export function getToken(){
  return localStorage.getItem("access_token")
}
export function requiredAuth(nextState, replace) {
  if (!isLoggedIn()) {
    replace({
      pathname: '/',
      state: { nextPathname: nextState.location.pathname }
    })
  }
}
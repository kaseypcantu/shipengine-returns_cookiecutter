export function getLocalStorageBlob() {
    let seReturnsAppString = localStorage.getItem("{{cookiecutter.directory_name}}_returns_app");
    if (!seReturnsAppString) {
        localStorage.setItem("se_returns_app", "{}");
        seReturnsAppString = "{}";
    }
    return JSON.parse(seReturnsAppString)
}

export function setLocalStorate(key, value) {
    const current = getLocalStorageBlob();
    current[key] = value;
    localStorage.setItem("se_retuns_app", JSON.stringify(current));
}

export function clearLocalStorage() {
    localStorage.removeItem("se_returns_app");
    localStorage.clear();
}

export function getLocalStorageItem(key) {
    const current = getLocalStorageBlob()
    return current[key]
}

// TODO: map these to your element ID's
export function clearInputs() {
  // From Address
  document.getElementById("from-name").value = "";
  document.getElementById("from-address1").value = "";
  document.getElementById("from-address2").value = "";
  document.getElementById("from-city").value = ""
  document.getElementById("from-state").value = "";
  document.getElementById("from-zip").value = ""

  // To Address
  document.getElementById("to-name").value = "";
  document.getElementById("to-address1").value = "";
  document.getElementById("to-address2").value = "";
  document.getElementById("to-city").value = "";
  document.getElementById("to-state").value = "";
  document.getElementById("to-zip").value = "";

  // Package Weight
  document.getElementById("weight-lbs").value = "";
  document.getElementById("weight-ounces").value = "";

  // Dimensions
  document.getElementById("length").value = "";
  document.getElementById("width").value = "";
  document.getElementById("height").value = "";
}
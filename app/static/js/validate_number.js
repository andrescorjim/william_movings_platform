function phonenumber(inputtxt) {
  var phoneNumber = /^((\+44)|(0)) ?\d{4} ?\d{6}$/;
  if (inputtxt.value.match(phoneNumber)) {
    return true;
  } else {
    alert("Not a valid Phone Number");
    return false;
  }
}


const card1 = document.getElementById('card-1');
const card2 = document.getElementById('card-2');
const card3 = document.getElementById('card-3');
//-------------------------------------------------------------------------
function loginInfo() {
	moveCards(card1, card2, card3);

};
//
function userInfo() {
	validateLoginForm().then ((isValid) => {
		if (isValid){
			moveCards(card2, card1, card3);
		}
	}
)};
//
function userInfo2() {
	moveCards(card2, card1, card3);
};
//
function contactInfo() {
	validateUserForm().then ((isValid) => {
		if (isValid){
			moveCards(card3, card1, card2);
		}
	}
)};
//-------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
	loginInfo();
});
//-------------------------------------------------------------------------
function moveCards (cardA, cardB, cardC) {
	cardA.style.opacity = "1";
	cardB.style.opacity = '0';
	cardC.style.opacity = '0';
	cardA.style.transform  =  "translateY(0%)";
	cardB.style.transform  = "translateY(-100%)";
	cardC.style.transform  = "translateY(-100%)";
}
//-------------------------------------------------------------------------
async function validateLoginForm() {
    const response = await fetch("/static/json/NameList.json");

    if (!response.ok) {
        console.log("Error in retrieval");
        return false;
    }

    const data = await response.json();
    const userNameList = data[0].name_list;
    const goodCodeList = data[1].code_list;

    const fUserName = document.forms["regForm"]["username"].value;
    const fPassword1 = document.forms["regForm"]["password1"].value;
    const fPassword2 = document.forms["regForm"]["password2"].value;
    const fHexKey = document.forms["regForm"]["hexkey"].value;

    if (isEmpty(fUserName)) {
        alert("Please enter a username");
        return false;
    }

    if (isInArray(fUserName, userNameList)) {
        alert("Username already exists");
        return false;
    }

    if (isEmpty(fPassword1) || fPassword2 !== fPassword1) {
        alert("Passwords do not match or contain the correct characters");
        return false;
    }

    if (isEmpty(fHexKey) || !isInArray(fHexKey, goodCodeList)) {
        alert("This key is invalid or has already been used");
        return false;
    }

    return true;
}

function isEmpty(value) {
    return value.trim() === "";
}

function isInArray(value, array) {
    return array.includes(value);
}
//
async function validateUserForm() {
	const response = await fetch("/static/json/NameList.json");
    console.log(response)   
	if (response.ok) {
		const data = await response.json();
		const userEmailList = data[2].email_list;
		let fFirstName = document.forms["regForm"]["first_name"].value;
		let fLastName = document.forms["regForm"]["last_name"].value;
		let femail = document.forms["regForm"]["email"].value;

		if (fFirstName == "") {
			alert("First name must be filled out");
			return false;
		};
		if (fLastName == "") {
			alert("Last name must be filled out");
			return false;
		};
		if (femail == "") {
			alert("please enter a valid email address")
			return false;
		};
		for (let emails of userEmailList){
			if (femail == emails){
				alert('Email already exist in this system')
				return false;
			}
		}
		if (!femail.includes('@') ){
			alert('Please enter a vlaid email')
			return false;
		};
		return true;
	} else {
		console.log("Error in retrieval");
	}
};
//-------------------------------------------------------------------------


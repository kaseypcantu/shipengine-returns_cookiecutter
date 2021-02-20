console.log("flask server funko Returns Portal CLIENT.JS LOADED!");

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        let notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            notification.parentNode.removeChild(notification);
        });
    });
});

const fullNameNode = document.querySelector("#name");
fullNameNode.addEventListener("blur", event => {
    localStorage.setItem("fullName", fullNameNode.value);
});

fullNameNode.addEventListener("change", event => {
    localStorage.setItem("fullName", fullNameNode.value);
});

const contactEmailNode = document.querySelector("#contact_email");
contactEmailNode.addEventListener("blur", event => {
    localStorage.setItem("contactEmail", contactEmailNode.value);
});

contactEmailNode.addEventListener("change", event => {
    localStorage.setItem("contactEmail", contactEmailNode.value);
});

const phoneNumberNode = document.querySelector("#phone");
phoneNumberNode.addEventListener("blur", event => {
    localStorage.setItem("contactPhone", phoneNumberNode.value);
});

phoneNumberNode.addEventListener("change", event => {
    localStorage.setItem("contactPhone", phoneNumberNode.value);
});
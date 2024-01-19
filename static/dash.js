// Function to switch between tabs
function show_table(cat){
    sessionStorage.setItem('active_tab', cat);
    rem = ["open","closed","all"].filter(item => item!=cat);

    active = document.getElementById("complaints_data-"+cat);
    active.style.display = "block";
    
    for(let x of rem){
        temp = document.getElementById("complaints_data-"+x);
        temp.style.display = "none";
    }

    // Highlight the active tab
    tabs = document.getElementById("tabs").children;
    for(let tab of tabs){
        if(tab.innerHTML.toLowerCase()==cat){
            tab.classList.add("active");
        }
        else{
            tab.classList.remove("active");
        }
    }
}

// Function to close a complaint using a POST request
function close_complaint(complaint_id){
    fetch("/dash/close", {
        method: "POST",
        headers: {'Content-Type': 'text/plain'},
        body: complaint_id
    })
    .then(response => response.text())
    .then(url => {
        // window.location.assign(url);
        location.reload();
    })
}

// Event listener to execute code when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    let active_tab = sessionStorage.getItem('active_tab');
    
    if (!active_tab) active_tab = 'open';
    
    show_table(active_tab);
})

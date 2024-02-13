function openTab(tabName) {
    let i, tabs;
    tabs = document.getElementsByClassName("tab");
    for (i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
}

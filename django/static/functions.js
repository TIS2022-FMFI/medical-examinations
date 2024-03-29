function search() {
    var input1, input2, input3, input4, input5, input6, filter1, filter2, filter3, filter4, filter5, filter6, table, tr, td1, td2, td3, td4, td5, td6, i;
    input1 = document.getElementById("name");
    input2 = document.getElementById("id");
    input3 = document.getElementById("posit");
    input4 = document.getElementById("depart");
    input5 = document.getElementById("city");
    input6 = document.getElementById("shift");
    filter1 = input1.value.toUpperCase();
    filter2 = input2.value.toUpperCase();
    filter3 = input3.value.toUpperCase();
    filter4 = input4.value.toUpperCase();
    filter5 = input5.value.toUpperCase();
    filter6 = input6.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        for (var n = 0; n < 6; n++){
            td = tr[i].getElementsByTagName("td");
            if(td){
                tr[i].style.display = "table-row ";
            }
        }
    }
    // Loop through all table rows, and hide those who don't match the search query
    console.log("TEST");
    console.log(input1, input2, input3, input4, input5, input6);
    console.log("TEST");
    for (i = 0; i < tr.length; i++) {
        if(input1.value === ""){
            break;
        }
        td1 = tr[i].getElementsByTagName("td")[0];
        if (td1) {
            if (td1.innerHTML.toUpperCase().indexOf(filter1) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    for (i = 0; i < tr.length; i++) {
        if (input2.value === "") {
            break;
        }
        td2 = tr[i].getElementsByTagName("td")[1];
        if (td2) {
            if (td2.innerHTML.toUpperCase().indexOf(filter2) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    for (i = 0; i < tr.length; i++) {
        if (input3.value === "--") {
            break;
        }
        td3 = tr[i].getElementsByTagName("td")[2];
        if (td3) {

            if (td3.innerHTML.toUpperCase().indexOf(filter3) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    for (i = 0; i < tr.length; i++) {
        if (input4.value === "--") {
            break;
        }
        td4 = tr[i].getElementsByTagName("td")[3];
        if (td4) {
            if (td4.innerHTML.toUpperCase().indexOf(filter4) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    for (i = 0; i < tr.length; i++) {
        if (input5.value === "--") {
            break;
        }
        td5 = tr[i].getElementsByTagName("td")[4];
        if (td5) {
            if (td5.innerHTML.toUpperCase().indexOf(filter5) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
    for (i = 0; i < tr.length; i++) {
        if (input6.value === "--") {
            break;
        }
        td6 = tr[i].getElementsByTagName("td")[5];
        if (td6) {
            if (td6.innerHTML.toUpperCase().indexOf(filter6) > -1) {
                continue;
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_name() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("name");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_id() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("id");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_position() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("posit");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_department() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("depart");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[3];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_city() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("city");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[4];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function search_by_shift() {
    // Declare variables 
    var input, filter, table, tr, td, i;
    input = document.getElementById("shift");
    filter = input.value.toUpperCase();
    table = document.getElementById("myList");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[5];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
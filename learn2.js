var complete = false;
var getData = [];
var edit = 0;

window.addEventListener("load", function () {
  (getData = JSON.parse(localStorage.getItem("temp2")) || []),
    showBarang(getData); //inisialisasi / Ambil Data Storage (GET)
});

function getComplete() {
  if (complete == true) {
    complete = false;

    console.log(complete);
    return;
  }
  complete = true;
  console.log(complete);
}

function clearField() {
  document.getElementById("inputBookTitle").value = "";
  document.getElementById("inputBookYear").value = "";
  document.getElementById("inputBookAuthor").value = "";
  complete = false;
  document.getElementById("inputBookIsComplete").checked = false;
}

function showBarang(data) {
  var nocom = document.querySelector("#incompleteBookshelfList"),
    com = document.querySelector("#completeBookshelfList");
  nocom.innerHTML = "";
  com.innerHTML = "";
  console.log(getData);
  data.forEach((item, idx) => {
    var row = document.createElement("article");
    var cell1 = document.createElement("h2");
    var cell2 = document.createElement("p");
    var cell3 = document.createElement("p");
    var cell4 = document.createElement("button");
    var cell5 = document.createElement("button");
    var cell6 = document.createElement("button");
    var div = document.createElement("div");
    var id = item.id;
    div.classList.add("action");
    row.classList.add("book_item");
    cell4.classList.add("red");
    cell5.classList.add("green");
    cell6.classList.add("blue");
    cell1.innerText = item.title;
    cell2.innerText = item.author;
    cell3.innerText = "Tahun: " + item.year;
    if (item.isComplete == true) {
      cell4.innerText = "Hapus Buku";
      cell5.innerText = "Belum Selesai Baca";
      cell6.innerHTML =
        "<button onclick='showBarangModel(" + idx + ")' >Edit</button>";
      cell4.addEventListener("click", function () {
        del(idx);
      });
      cell5.addEventListener("click", function () {
        notDone(idx);
      });

      row.appendChild(cell1),
        row.appendChild(cell2),
        row.appendChild(cell3),
        div.appendChild(cell4),
        div.appendChild(cell5),
        div.appendChild(cell6),
        row.appendChild(div);
      com.appendChild(row);
    } else {
      cell4.innerText = "Hapus Buku";
      cell5.innerText = "Selesai Baca";
      cell6.innerHTML =
        "<button onclick='showBarangModel(" + idx + ")'>Edit</button>";
      cell5.addEventListener("click", function () {
        done(idx);
      });

      cell4.addEventListener("click", function () {
        del(idx);
      });
      row.appendChild(cell1),
        row.appendChild(cell2),
        row.appendChild(cell3),
        div.appendChild(cell4),
        div.appendChild(cell5),
        div.appendChild(cell6),
        row.appendChild(div),
        nocom.appendChild(row);
    }
  });
}

function findBook() {
  const n = document.getElementById("searchBookTitle").value;
  (query = n),
    query
      ? showBarang(
          getData.filter(function (getData) {
            return getData.title.toLowerCase().includes(query.toLowerCase());
          })
        )
      : showBarang(getData);

  // query?  showBarang(
  //   getData.filter(function (getData) {
  //     return getData.title.toLowerCase().includes(query.toLowerCase());
  //   })
  // ) : query=="ryan" ? "test" : showBarang(getData)

  // if(query){
  //   showBarang(
  //     getData.filter(function (getData) {
  //       return getData.title.toLowerCase().includes(query.toLowerCase());
  //     })
  //   )
  // }else if (query=="ryan"){
  //   return "test"
  // }

  // else{
  //   showBarang(getData)
  // }
}

const updateStatus = (i, isComplete = false) => {
  if (getData[i]["isComplete"]) {
    getData[i]["isComplete"] = isComplete;
    return alert(
      getData[i]["title"] + ` ${isComplete ? "Telah" : "Belum"} Selesai Di Baca`
    );
  }
  return alert("Data tidak ditemukan");
};

// function notDone(i) {
//   getData[i]["isComplete"] = false;
//   alert(getData[i]["title"] + " Telah Belum Selesai Di Baca");
//   postData();
// }

// function done(i) {
//   getData[i]["isComplete"] = true;
//   alert(getData[i]["title"] + " Telah Selesai Di Baca");
//   postData();
// }

function del(i) {
  alert(getData[i]["title"] + " Telah Di Hapus");
  getData.splice(i, 1);
  postData();
}
function showBarangModel(i) {
  document.getElementById("inputBookTitle2").value = getData[i]["title"];
  document.getElementById("inputBookYear2").value = getData[i]["year"];
  document.getElementById("inputBookAuthor2").value = getData[i]["author"];
  document.getElementById("editShow").hidden = false;
  edit = i;
  document.getElementById("inputBookTitle2").focus();
}
function batalEdit() {
  document.getElementById("editShow").hidden = true;
}

function submitDataEdit() {
  // localhost:3000/user?add=true

  // let params = (new URL(document.location)).searchParams;
  // let isadd = params.get("add")

  // if(isadd){
  //   var title = document.getElementById("inputBookTitle2").value;
  //   var author = document.getElementById("inputBookAuthor2").value;
  //   var year = document.getElementById("inputBookYear2").value;
  //   getData[edit]["title"] = title;
  //   getData[edit]["author"] = author;
  //   getData[edit]["year"] = year;
  //   postData();
  //   alert(getData[edit]["title"] + " Telah Di Edit");
  //   document.getElementById("editShow").hidden = true;
  //   return
  // }
  // return alert("Bukan Edit");
  if (edit == 0) {
    return alert("Bukan Edit");
  }
  var title = document.getElementById("inputBookTitle2").value;
  var author = document.getElementById("inputBookAuthor2").value;
  var year = document.getElementById("inputBookYear2").value;
  getData[edit]["title"] = title;
  getData[edit]["author"] = author;
  getData[edit]["year"] = year;
  postData();
  alert(getData[edit]["title"] + " Telah Di Edit");
  document.getElementById("editShow").hidden = true;
  return;
}

function submitData() {
  var title = document.getElementById("inputBookTitle").value;
  var author = document.getElementById("inputBookAuthor").value;
  var year = document.getElementById("inputBookYear").value;
  var data = {
    id: +new Date(),
    title: title,
    author: author,
    year: year,
    isComplete: complete,
  };
  getData.push(data);
  clearField();
  alert("Buku Di Tambahkan [!]");

  postData(getData);
}

function postData() {
  !(function (getData) {
    localStorage.setItem("temp2", JSON.stringify(getData));
  })(getData),
    showBarang(getData);
}

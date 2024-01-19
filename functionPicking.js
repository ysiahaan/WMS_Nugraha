let jumlah = 0,
  jumlahscan = 0,
  itsFirst = 0,
  btnStock = "";
var fisrt = 0,
  kodebarang = "",
  barcode = "",
  kodebrgpack = "",
  kodebrgkarton = "",
  scan = "",
  jmlkarton = 0,
  jmlperkarton = 0,
  isiData = [],
  namabarang = "",
  satuan = "",
  stokkarton = GetURLParameter("stokkarton"),
  stokpcs = "";
let jumlahpermintaan = GetURLParameter("jumlahbarang");
var kodebarang = GetURLParameter("kodebarang");
var lokasi = GetURLParameter("lokasi");
var jmlItem = GetURLParameter("jmlItem");
var jumlahorder = GetURLParameter("jumlahorder");
var index = 0;
var user = GetURLParameter("namalogin");
var level = GetURLParameter("level");
var so = GetURLParameter("so");
var iddsalesorder = GetURLParameter("id");
kol = document.createElement("tr");
cell = document.createElement("div");
cellcall = document.createElement("div");
// var UrlApi = "http://zeppy2.ath.cx:5101";
// var UrlApi = "http://zeppy2.ath.cx:5104"; //server mulai2
var UrlApi = "http://localhost:3301";
// var UrlApi = "http://192.168.14.137:3301"; //mulai2 3301
document.addEventListener("deviceready", onDeviceReady, false);
document.addEventListener("backbutton", function (e) {
  e.preventDefault();
});

var url =
  UrlApi +
  "/nug_api/getBarangdet?kodebarang=" +
  kodebarang +
  "&lokasi=" +
  lokasi;

fetch(url)
  .then((response) => {
    if (!response.ok) {
      alert("Terjadi Kesalahan Dalam Respons.");
      return;
      throw new Error("Terjadi kesalahan dalam respons.");
    }
    return response.json();
  })
  .then((data) => {
    // Sukses, data dari server ada di sini
    //alert("Sukses, Request Data.");
    document.getElementById("input1").focus();
    // console.log(data);
    var obj = data;
    var err = data.error;
    var msg = data.msg;
    isiData = obj.data.rows;
    if (isiData[0]["kodebrgpack"] == "tidak") {
      view();
      alert("Barang Belum Di Barangdet");
    }
    view();
  })
  .catch((error) => {
    // Menangani kesalahan
    console.error("Terjadi kesalahan Server", error);
    // alert("Request Gagal." + " (GET:/nug_api/getDSOScan)");
    return;
  });

const view = () => {
  jmlkarton = isiData[0]["jmlkarton"];
  namabarang = isiData[0]["namabarang"];
  satuan = isiData[0]["satuan"];
  barcode = isiData[0]["barcode"];
  jmlperkarton = jumlahpermintaan / jmlkarton;
  kodebrgpack = isiData[0]["kodebrgpack"];
  kodebrgkarton = isiData[0]["kodebrgkarton"];
  stokpcs = isiData[0]["totalpcs"];
  item = jmlItem;
  tempIndex = item;
  tempIndex--;

  // SO
  var theTabel = document.getElementById("listSO");
  theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
  var tbody = document.createElement("tbody");
  theTabel.appendChild(tbody);
  var row = document.createElement("tr");
  var cell1 = document.createElement("div");
  cell1.classList.add("styleSO");
  cell1.innerHTML = "SO : " + so;
  row.appendChild(cell1);
  tbody.appendChild(row);

  // List
  var theTabel = document.getElementById("listBarang");
  theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
  var tbody = document.createElement("tbody");
  theTabel.appendChild(tbody);
  var row = document.createElement("tr");
  var cell2 = document.createElement("div");
  var cell3 = document.createElement("div");

  var div1 = document.createElement("div");
  var cellpcs = document.createElement("p");
  var cell5 = document.createElement("p");

  div1.classList.add("stylediv1");
  cellpcs.classList.add("stylecellkarton");
  cell5.classList.add("stylecellkarton");

  var cell4 = document.createElement("a");
  var textSatuan = satuan;
  cell2.classList.add("styleNamabrg");
  cell3.classList.add("styleOrder");
  cell4.classList.add("stylePCS");
  cell5.classList.add("styleStokPicking");
  cell2.innerHTML = namabarang;
  cell4.innerHTML = textSatuan;
  cell3.innerHTML = "Jumlah Order : " + jumlahpermintaan + "  " + cell4;

  cellpcs.innerHTML = `Stok Lepasan : ${stokpcs} ${satuan}`;
  cell5.innerHTML = `Stok Karton : ${stokkarton} Q`;

  row.appendChild(cell2);
  row.appendChild(cell3);
  cell3.appendChild(cell4);
  div1.appendChild(cellpcs);
  div1.appendChild(cell5);
  row.appendChild(div1);
  tbody.appendChild(row);

  //Icon
  var theTabel = document.getElementById("tableIcon");
  theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
  var tbody = document.createElement("tbody");
  theTabel.appendChild(tbody);
  var row = document.createElement("tr");
  var icon = document.createElement("div");
  icon.classList.add("imageIcon");
  icon.innerHTML = "<img src='img/scanning.png' style='height: 200px;'>";
  row.appendChild(icon);
  tbody.appendChild(row);

  // Button
  tblButton();
};

function onDeviceReady() {
  //unitTesting();
}
function GetURLParameter(sParam) {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split("&");
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split("=");
    if (sParameterName[0] == sParam) {
      return sParameterName[1];
    }
  }
}

//----------------------------------------------------------------------------------------------------------------------------------------
function exeScan() {
  var temp = document.getElementById("input1").value;
  scan = temp.trim();
  if (scan == "") {
    alert("Input Data Terlebih Dahulu [!]");
  } else {
    if (isNaN(jumlahscan)) {
      jumlahscan = 0;
    }
    if (scan == barcode) {
      //barcode
      jumlah = isiData[0]["jumlahbrg"];
      jumlahscan = jumlahscan + parseInt(jumlah);
    } else if (scan == kodebrgpack) {
      //pack
      jumlah = isiData[0]["jmlpack"];
      jumlahscan = jumlahscan + parseInt(jumlah);
    } else if (scan == kodebrgkarton) {
      //karton
      jumlah = isiData[0]["jmlkarton"];
      jumlahscan = jumlahscan + parseInt(jumlah);
    } else {
      alert("Barcode Tidak Ditemukan [!]");
      clearBarcode();

      ////console.log("Barcode Tidak Ditemukan [!]");
    }
    ////console.log("ini adalah jumlah scan : ", jumlahscan);
    if (jumlahscan > 0) {
      exeTambah();
    }
  }
}

function myFocus() {
  document.getElementById("inputScanValue").focus();
}

function exeTambah() {
  const inputScanValue = document.getElementById("inputScanValue");
  if (inputScanValue == "") {
    //console.log("kosong");
    alert("Field Kosong [!]");
    return;
  }
  var theTabel = document.getElementById("tableTambah");
  tbody = theTabel.getElementsByTagName("tbody")[0];
  var cell1 = document.createElement("div");
  cell1.classList.add("inputStyle4");
  cell1.innerHTML =
    "<input onsubmit='exeTambahJumlahScan()' class='inputStyle4' type='text' id='input2' name='input2' value=" +
    jumlahscan +
    ">";
  document.getElementById(
    "valueScan"
  ).innerHTML = `Item Picking : ${jumlahscan}`;
  inputScanValue.value = jumlahscan;
  btnStock = document.getElementsByName("btnStock")[0];
  document.getElementById("inputScanValue").focus();
  clearBarcode();
  tblButton();
}

function clearBarcode() {
  ////console.log("CLEAR BARCODE");
  document.getElementById("input1").value = "";
}

function exeTambahJumlahScan() {
  ////console.log("sebelum : ", jumlah, jumlahscan);
  jumlah = document.getElementById("inputScanValue").value;
  jumlahscan = parseInt(jumlah);
  document.getElementById("inputScanValue").value = jumlah;
  document.getElementById(
    "valueScan"
  ).innerHTML = `Item Picking new: ${jumlah}`;
  ////console.log("sesudah : ", jumlah, jumlahscan);
  document.getElementsByName("btnStock").innerHTML = "";
  document.getElementById("input1").focus();
}

function tblButton() {
  if (fisrt == 1) {
    kol.appendChild(cell);
  }
  ////console.log(jumlahorder, item);
  if (item == 0) {
    if (jumlahscan < jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cellcall.classList.add("styleButton22");
      cell.classList.add("styleButton22");
      kol.classList.add("styleKol");
      cell.innerHTML =
        "<button onclick='putPicking()' name='btnStock' id='btnStock' type='button' class='btn btn-primary'>Stok Habis, Picking Selesai</button>";
      cellcall.innerHTML =
        "<button onclick='callReffiler()' name='btnStock2' id='btnStock2' type='button' class='btn btn-primary'>Stok Habis, Refill Stok</button>";
      kol.appendChild(cell);
      kol.appendChild(cellcall);
      cellcall.hidden = false;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    } else if (jumlahscan == jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cell.classList.add("styleButton22");
      cell.innerHTML =
        "<button onclick='putPicking()' name='btnStock' id='btnStock' type='button' class='btn btn-primary'>Picking Selesai</button>";
      kol.appendChild(cell);
      cellcall.hidden = true;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    } else if (jumlahscan > jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cell.classList.add("styleButton22");
      cell.innerHTML =
        "<button name='btnStock' id='btnStock' type='button'  class='btn btn-danger'>Jumlah Picking Berlebih [!]</button>";
      kol.appendChild(cell);
      cellcall.hidden = true;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    }
  } else {
    if (jumlahscan < jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cellcall.classList.add("styleButton22");
      cell.classList.add("styleButton22");
      kol.classList.add("styleKol");
      cell.innerHTML =
        "<button onclick='putPicking()' name='btnStock' id='btnStock' type='button' class='btn btn-primary'>Stok Habis, Lokasi Berikutnya</button>";
      cellcall.innerHTML =
        "<button onclick='callReffiler()' name='btnStock2' id='btnStock2' type='button' class='btn btn-success'>Stok Habis, Refill Stok</button>";
      kol.appendChild(cell);
      kol.appendChild(cellcall);
      cellcall.hidden = false;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    } else if (jumlahscan == jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cell.classList.add("styleButton22");
      cell.innerHTML =
        "<button onclick='putPicking()' name='btnStock' id='btnStock' type='button' class='btn btn-primary'>Next Lokasi</button>";
      kol.appendChild(cell);
      cellcall.hidden = true;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    } else if (jumlahscan > jumlahpermintaan) {
      var theTabel = document.getElementById("tableButton");
      theTabel.removeChild(theTabel.getElementsByTagName("tbody")[0]);
      var tbody = document.createElement("tbody");
      theTabel.appendChild(tbody);
      cell.classList.add("styleButton22");
      cell.innerHTML =
        "<button  name='btnStock' id='btnStock' type='button' class='btn btn-danger'>Jumlah Picking Berlebih [!]</button>";
      kol.appendChild(cell);
      cellcall.hidden = true;
      tbody.appendChild(kol);
      fisrt = 1;
      return;
    }
  }
}

const callReffiler = () => {
  var ceklok = lokasi.substring(0, 1);
  if (ceklok == 9 || ceklok == 8) {
    putPicking();
    return;
  }
  if (stokkarton == 0) {
    alert("Stok Karton Kosong, Lokasi Berikutnya");
    putPicking();
    return;
  }
  var url =
    UrlApi +
    "/nug_api/confirmStok?lokasi=" +
    lokasi +
    "&kodebarang=" +
    kodebarang +
    "&noso=" +
    so +
    "&iddsales=" +
    iddsalesorder;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        alert("Terjadi kesalahan Dalam Respons.");
        throw new Error("Terjadi kesalahan dalam respons.");
      }
      return response.json();
    })
    .then((data) => {
      location.href =
        "picking_scanLokasi.html?namalogin=" +
        user +
        "&so=" +
        so +
        "&jumlahorder=" +
        jumlahorder +
        "&jmlItem=" +
        jmlItem +
        "&level=" +
        level;
    })
    .catch((error) => {
      alert("Request Gagal");
    });
};

function putPicking() {
  document.getElementById("btnStock").disabled = true;
  console.log("========function Put Picking===========");
  console.log("noso : ", so);
  console.log("index : ", index);
  console.log("jumlahscan : ", jumlahscan);
  console.log("picker : ", user);
  console.log("Jumlah Order : ", jumlahpermintaan);
  console.log("Lokasi : ", lokasi);
  console.log("kodebar : ", kodebarang);
  console.log("jmlItem : ", jmlItem);
  console.log("iddsalesorder : ", iddsalesorder);
  jmlperkarton = jumlahscan / jmlkarton;
  console.log("jumlah per item : ", jmlperkarton);
  if (jumlahscan < jumlahpermintaan) {
    if (confirm("Jumlah Permintaan Kurang, Yakin Lanjut ? ")) {
    } else {
      document.getElementById("btnStock").disabled = false;
      return;
    }
  } else if (jumlahscan > jumlahpermintaan) {
    if (confirm("Jumlah Scan Lebih Dari Jumlah Permintaan, Yakin Lanjut ?")) {
    } else {
      document.getElementById("btnStock").disabled = false;
      return;
    }
  }
  var url =
    UrlApi +
    "/nug_api/pickingResi?noso=" +
    so +
    "&index=" +
    index +
    "&jumlahScan=" +
    jumlahscan +
    "&picker=" +
    user +
    "&lokasi=" +
    lokasi +
    "&kodebar=" +
    kodebarang +
    "&jmlScanKarton=" +
    jmlperkarton +
    "&jmlItem=" +
    jmlItem +
    "&jumlahOrder=" +
    jumlahorder +
    "&iddsalesorder=" +
    iddsalesorder;

  fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        alert("Terjadi kesalahan Dalam Respons.");
        throw new Error("Terjadi kesalahan dalam respons.");
      }
      return response.json();
    })
    .then((data) => {
      // Sukses, data dari server ada di sini
      console.log("Sukses");
      if (jmlItem == 0) {
        alert("SO Selesai, Terima Kasih");

        location.href =
          "picking_scanSO.html?namalogin=" + user + "&level=" + level;
        return;
      }
      getNextLocation();
    })
    .catch((error) => {
      // Menangani kesalahan
      document.getElementById("btnStock").disabled = false;
      alert("Request Gagal. (PUT:/nug_api/getDSOScan)");

      //console.log("Terjadi kesalahan");
    });
}

function getNextLocation() {
  jumlahorder++;
  jmlItem--;
  location.href =
    "picking_scanLokasi.html?namalogin=" +
    user +
    "&so=" +
    so +
    "&jumlahorder=" +
    jumlahorder +
    "&jmlItem=" +
    jmlItem +
    "&level=" +
    level;
}

function exeDashboard() {
  if (confirm("Confirm")) {
    location.href = "dashboard.html?namalogin=" + user + "&level=" + level;
  } else {
    return false;
  }
}
function exeHome() {
  if (confirm("Confirm")) {
    location.href = "picking_scanSO.html?namalogin=" + user + "&level=" + level;
  } else {
    return false;
  }
}
function exeBack() {
  if (confirm("Confirm")) {
    location.href = "picking_scanSO.html?namalogin=" + user + "&level=" + level;
  } else {
    return false;
  }
}
function exeRefresh() {
  document.getElementById("input1").focus();
  location.reload();
}

const unitTesting = () => {
  jumlahscan = jumlahpermintaan;
  putPicking();
};

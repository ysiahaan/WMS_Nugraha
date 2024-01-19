let jumlah = 0;
var scan = 0;
var user = GetURLParameter("namalogin");
var so = GetURLParameter("so");
var level = GetURLParameter("level");
var packingIndex = "";
// var UrlApi = "http://zeppy2.ath.cx:5101";
// var UrlApi = "http://zeppy2.ath.cx:5104"; //server mulai2
var UrlApi = "http://localhost:3301";
// var UrlApi = "http://192.168.14.137:3301"; //mulai2 3301
document.addEventListener("deviceready", onDeviceReady, false);
document.addEventListener("backbutton", function (e) {
  e.preventDefault();
});

function onDeviceReady() {
  document.getElementById("valueSO").innerHTML = `SO : ${so}`;
  const inputScanValue = document.getElementById("inputScanValue");
  inputScanValue.value = "";
  document.getElementById("inputBarcode").focus();
  getNomerPacking();
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

function getNomerPacking() {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", UrlApi + "/nug_api/getNomerPacking?noso=" + so);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  let data = "";
  ////console.log(data)
  xhr.send(data);
  xhr.onload = function () {
    console.log(this.responseText);
    var obj = JSON.parse(this.responseText);
    var getData = obj.data.rows;
    var getDataTotal = getData[0]["stat1"];
    if (getDataTotal == "") {
      packingIndex = 1;
      document.getElementById(
        "idIndex"
      ).innerHTML = `Nomer Packing Sekarang ${parseInt(packingIndex)}`;
      return;
    }
    var getData = obj.data.rows;
    packingIndex = getData[0]["stat1"];

    document.getElementById(
      "idIndex"
    ).innerHTML = `Nomer Packing Sekarang ${parseInt(packingIndex)}`;
  };
}

function exeScan() {
  scan = document.getElementById("inputBarcode").value;
  //  console.log("------------ ", scan);
  if (scan == "") {
    alert("Scan Barcode Kosong [!]");
  } else {
    getJumlah();
    return;
  }
}

function getJumlah() {
  //  console.log("========== ", scan);
  let xhr = new XMLHttpRequest();
  xhr.open("GET", UrlApi + "/nug_api/barangdet?kodebrg=" + scan);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  let data = "kodebrg=" + scan;
  xhr.send(data);
  xhr.onload = function () {
    //  console.log(this.responseText);
    var obj = JSON.parse(this.responseText);
    var dataMain = obj.data.rows;
    if (dataMain.length == 0) {
      alert("Barcode Tidak Ada");
      clearBarcode();
      return;
    } else {
      jumlah = dataMain[0]["jumlah"];
      //  console.log(jumlah);
      myFocus();
      putPacking();
    }
    return;
  };
}

function putPacking() {
  //  console.log(">>>>>>>>>>>> ", scan);
  let xhr = new XMLHttpRequest();
  xhr.open(
    "PUT",
    UrlApi +
      "/nug_api/getDSOCheck?noso=" +
      so +
      "&barScan=" +
      scan +
      "&checker=" +
      user +
      "&jumlah=" +
      jumlah +
      "&index=" +
      packingIndex
  );
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  let data =
    "noso=" +
    so +
    "&barScan=" +
    scan +
    "&checker=" +
    user +
    "&jumlah=" +
    jumlah +
    "&index=" +
    packingIndex;
  xhr.send(data);
  xhr.onload = function () {
    //  console.log(this.responseText);
    var obj = JSON.parse(this.responseText);
    var err = obj.error;
    var msg = obj.msg;
    if (err == "true") {
      alert(msg);
      document.getElementById("inputBarcode").focus();
      clearBarcode();
      return;
    }
    var dataMain = obj.data.rows;
    var namabarang = dataMain[0]["nama_barang"];
    var barcode = scan;
    var picking = dataMain[0]["total_brg"];
    var packing = dataMain[0]["noPack"];
    console.log(packing);
    var sisa = dataMain[0]["sisa"];
    var satuan = dataMain[0]["satuan"];
    if (dataMain.length == 0) {
      alert("Barcode Tidak Dalam Daftar SO");
      clearBarcode();
    } else {
      document.getElementById("idNamaBarang").innerHTML = `${namabarang}`;
      document.getElementById("idBarcode").innerHTML = `${barcode}`;
      document.getElementById("idPicking").innerHTML = `Picking : ${picking}`;
      document.getElementById("idNoPax").innerHTML = `No Pax :  ${packing}`;

      document.getElementById("idSisa1").innerHTML = `SISA `;
      document.getElementById("idSisa").innerHTML = ` ${sisa}`;
      document.getElementById("idSisa2").innerHTML = ` ${satuan}`;
      document.getElementById(
        "idIndex"
      ).innerHTML = `Nomer Packing Sekarang ${parseInt(packingIndex)}`;
    }
    clearBarcode();
  };
}

function myFocus() {
  document.getElementById("inputScanValue").focus();
}

function lanjutPacking() {
  let xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    UrlApi + "/nug_api/getDSOPack?noso=" + so + "&nopack=" + packingIndex
  );
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  let data = "noso=" + so + "&nopack=" + packingIndex;
  xhr.send(data);
  xhr.onload = function () {
    ////console.log(this.responseText);
    var obj = JSON.parse(this.responseText);
    var dataMain = obj.data.rows;
    var validasiNoPak = obj.data.total;
    ////console.log(validasiNoPak);
    if (validasiNoPak == "0") {
      alert(
        "Pakai Nomor Pakcing Sekarang, Karna Masih Belum Diisi \nLanjut Scan Barang"
      );
      return;
    } else {
      packingIndex++;
      ////console.log(packingIndex);
      alert("Nomor Packing Baru : " + packingIndex);
      document.getElementById(
        "idNoPax"
      ).innerHTML = `No Pax :  ${packingIndex}`;
      document.getElementById(
        "idIndex"
      ).innerHTML = `Nomer Packing Sekarang ${parseInt(packingIndex)}`;
    }
  };
}

function selesaiPacking() {
  // alert("Packing Selesai");
  // location.href = "packing_scanSO.html?namalogin=" + user + "&level=" + level;
  let xhr = new XMLHttpRequest();
  xhr.open("GET", UrlApi + "/nug_api/getDSOCheckFull?noso=" + so);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  let data = "noso=" + so;
  xhr.send(data);
  xhr.onload = function () {
    //  console.log(this.responseText);
    var obj = JSON.parse(this.responseText);
    var dataMain = obj.data.rows;
    var validasiNoPak = obj.error;
    ////console.log(validasiNoPak);
    if (validasiNoPak == "false") {
      alert("Packing Selesai");
      location.href =
        "packing_scanSO.html?namalogin=" + user + "&level=" + level;
      return;
    } else {
      alert("Packing Belum Selesai ");
      return;
    }
  };
}

function addJumlahText() {
  var inputScanValue = document.getElementById("inputScanValue").value;
  jumlah = inputScanValue;
  document.getElementById("inputScanValue").innerHTML = `${jumlah}`;
  ////console.log(jumlah);
  document.getElementById("inputBarcode").focus();
  putPacking();
}

function clearBarcode() {
  ////console.log("CLEAR BARCODE");
  document.getElementById("inputBarcode").value = "";
  document.getElementById("inputScanValue").value = "";
}

function exeDashboard() {
  location.href = "dashboard.html?namalogin=" + user + "&level=" + level;
}
function exeHome() {
  location.href = "packing_scanSO.html?namalogin=" + user + "&level=" + level;
}
function exeBack() {
  location.href = "packing_scanSO.html?namalogin=" + user + "&level=" + level;
}
function exeRefresh() {
  //location.href="scan_barang.html?namalogin="+user+"&level="+level
  document.location.reload(true);
}

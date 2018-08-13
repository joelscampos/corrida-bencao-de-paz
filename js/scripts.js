$('document').ready(function(){
  
  // FIXE THE NAVBAR ON THE TOP.
  $(window).scroll(function(){
    
    if ($(window).scrollTop() > 0) {
      
      $('.navbar').addClass('navbar-fixed-top');
    }
    if ($(window).scrollTop() < 1) {
      $('.navbar').removeClass('navbar-fixed-top');
    }
  });  
  
  
  $('#link-group-ad, #link-group-eh, #link-group-il, #link-group-mp, #link-group-qt, #link-group-uz').click(function(){
    
    shaddowThisMenu($(this));
    makeRequest($(this));
  });
  
  
  // TRIGGER PESQUISA
  $("#search-button").click(function() {
    makeRequest($(this));
  });
  
  // TRIGGER PESQUISA
  $("#search-text").keypress(function(e) {
    if (e.which == 13) {
      makeRequest($(this));
    }
  });
  
  
  
  $("#myModal").draggable({
    handle: ".modal-header"
  });
  
  $("#atletaModal").draggable({
    handle: ".modal-header"
  });
  
    
  $("#myModal #btn-salva").click(function() {
    
    /*alert("Salvar, confirmar, e excluir a linha.");*/
    executaEntrega($(this));
  });
  
  /*$("#myModal #btn-cancela").click(function() {*/
  $("#myModal").not("#btn-cancela").on("hide.bs.modal", function() {
    desmarcaCheckbox($(this));
  });

}); // $('document').ready(function()


var desmarcaCheckbox = function(currentElement) {
  
  var myModal = currentElement;
  var idAtleta = myModal.children("input#idAtleta").val();
  $("tr#" + idAtleta).find("input[type=checkbox]").prop("checked", false);
  $(myModal).find("input[type=hidden]").remove();

} // desmarcaCheckbox

var executaEntrega = function(currentElement) {
  
  var url = "https://ip4supg4x5.execute-api.us-east-2.amazonaws.com/dev/atleta/atualiza";
  var myModal = currentElement.parent().parent().parent().parent();
  var idAtleta = myModal.children("input#idAtleta").val();
  var nomeAtleta = myModal.children("input#nomeAtleta").val();
  var entreguePara = myModal.children(".modal-dialog").children(".modal-content").children(".modal-body").children("#entregue-para");
  
  // clear the field "Entregue para"
  myModal.children(".modal-dialog").children(".modal-content").children(".modal-body").children("#entregue-para").val("");
  
  // NOME DA PESSOA PARA QUAL FOI ENTREGUE O KIT.
  if (entreguePara.val() === "") {
    entreguePara = entreguePara.attr("placeholder");
  } else {
    entreguePara = entreguePara.val();
  }
  
  var currentdate = new Date(); 
  var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
  
  
  
  var dataToBeSent = JSON.stringify({"inscricoes":[
    {
      "Numero_de_inscricao": idAtleta.toString(), 
      "Nome_Completo": nomeAtleta, 
      "Kit_Entregue": "True", 
      "Nome_Entregue": entreguePara,
      "Data_Entregue": datetime.toString()}
    ]});
  /*$("#entregue-para").attr("placeholder",nomeAtleta);*/
  $.post(url, dataToBeSent, function( data, status ){
    
    if (status == "success") {
      // REMOVE THE ROW FROM THE TABLE.
      $("tr#" + idAtleta).remove();
      
      $('#myModal').modal('hide');
    } else {
      alert("Erro ao gravar. Atualize a página.");
      console.log(data);
    }
    
    $(myModal).find("input[type=hidden]").remove();
  }, "json");
  
} // executaEntrega


var makeRequest = function(currentElement) {
  
  var url = "https://ip4supg4x5.execute-api.us-east-2.amazonaws.com/dev/";
  var elementType = "";
  var totalSelecionado = "";
  var elementId = currentElement.attr("id");
      
  
  // Parametros da URL de pesquisa por grupo.
  if (elementId.includes("link-group")) {    
    elementType = "Group";    
    url += "atleta/pesquisaGrupoNome?idGrupo=" + elementId.replace("link-group-","");    
  }
  /*else if (elementId == "search-button") {    
    elementType = "BuscaNome";
    value = document.getElementById("search-text").value;
    if (value === "")
      return;
    url += "atleta/pesquisa?Nome_Completo=" + value;
  }*/
  else {
    value = document.getElementById("search-text").value;
    if (value === "")
      return;
    url += "atleta/pesquisa?Pesquisa_texto=" + value;
  }
  
  if ($("#somenteNaoEntregues").prop("checked")) {
    url += "&somenteNaoEntregues=True";
  }
  else {
    url += "&somenteNaoEntregues=False";
  }
  
  $.getJSON(url, function( data ){
    
    putJSONOnTheTable(data);      

    // Update the group's total.
    if (elementType === "Group") {
      updateTotalGroupLetters(currentElement, data["TotalSelecionado"]);
    }
    
    // CLICK & HOLD
    /*$("tr").mouseup(function() {
      // Clear timeout
      clearTimeout(pressTimer);
      return false;
    });
    
    // CLICK & HOLD
    $("tr").mousedown(function() {
      currentElement = this;
      
      // Set timeout
      pressTimer = window.setTimeout(function(e) {
        
        var nomeAtleta = currentElement.children[1].innerHTML;
        var idAtleta = currentElement.getAttribute("id").toString();
        
        exibeDetalhesAtleta(idAtleta, nomeAtleta);
        
      }, 5000);
      return false;
    });*/
    
    // CLICK IN THE ROW, TO SEE THE DETAILS.
    $("td").not("td:has(input)").click(function() {
      
      var nomeAtleta = this.parentElement.children[1].innerHTML;
      var idAtleta = this.parentElement.getAttribute("id").toString();
        
      exibeDetalhesAtleta(idAtleta, nomeAtleta);

    });

    
    
    // WHEN SOMETHING ON THE <input> ELEMENT CHANGES.
    $("table").on("change", "input", function(event) {

      // Reference: https://getbootstrap.com/docs/3.3/javascript/
      // this will contain a reference to the checkbox   
      if (this.checked) {
        var nomeAtleta = this.parentElement.parentElement.children[1].innerHTML;
        var idAtleta = this.parentElement.parentElement.getAttribute("id").toString();
        
        
        $("#entregue-para").attr("placeholder",nomeAtleta);
        
        idAtleta = '<input type="hidden" id="idAtleta" value="' + idAtleta + '">';
        nomeAtleta = '<input type="hidden" id="nomeAtleta" value="' + nomeAtleta + '">';
        
        
        $("#myModal").append(idAtleta);
        $("#myModal").append(nomeAtleta);
        
        // You cannot click outside of this modal to close it.
        $("#myModal").modal({backdrop: "static"});
        $('#myModal').modal('show');
        
      } else {
        /*Checa se não resta nenhum checkbox marcado, e envia.*/
        /*$('#myModal').modal('toggle');
        $('#myModal').modal('hide');*/
      }

    }); // $("table").on

  }); // $.getJSON
} //makeRequest


var exibeDetalhesAtleta = function(idAtleta, nomeAtleta) {
  
  var url = "https://ip4supg4x5.execute-api.us-east-2.amazonaws.com/dev/atleta/detalhe?Numero_de_inscricao=" + idAtleta.toString();
  
  $.getJSON(url, function( data ){
    
    var atleta = data["Items"][0];
    
    var modalContent = '<pre>';
      modalContent += '<p><strong>      Inscricao: </strong>' + atleta["Numero_de_inscricao"] + '</p>';
      modalContent += '<p><strong>Grupo Categoria: </strong>' + atleta["Grupo_Categoria"] + '</p>';
      modalContent += '<p><strong>      Categoria: </strong>' + atleta["Categoria"] + '</p>';
      modalContent += '<p><strong>         Atleta: </strong>' + nomeAtleta + '</p>';
      modalContent += '<p><strong>     Nascimento: </strong>' + atleta["Data_de_nascimento"] + '</p>';
      modalContent += '<p><strong>         E-mail: </strong>' + atleta["E_mail"] + '</p>';
      modalContent += '<p><strong> Tipo Documento: </strong>' + atleta["Tipo_de_Documento"] + '</p>';
      modalContent += '<p><strong>      Documento: </strong>' + atleta["Documento"] + '</p>';
      modalContent += '<p><strong>           Sexo: </strong>' + atleta["Sexo"] + '</p>';
      modalContent += '<p><strong>       CAMISETA: </strong>' + atleta["CAMISETA"] + '</p>';
      modalContent += '<p><strong>  CAMISETA KIDS: </strong>' + atleta["CAMISETA_KIDS"] + '</p>';
      modalContent += '</pre><pre>';

    if (atleta["Kit_Entregue"] == "False") {
      modalContent += '<p><strong> Kit Entregue: </strong>' + "NÃO" + '</p>';
      modalContent += '<p><strong>Entregue para: </strong>' + "" + '</p>';
      modalContent += '<p><strong>Data entregue: </strong>' + "" + '</p>';
    } else {
      modalContent += '<p><strong> Kit Entregue: </strong>' + "SIM" + '</p>';
      modalContent += '<p><strong>Entregue para: </strong>' + atleta["Nome_Entregue"] + '</p>';
      modalContent += '<p><strong>Data entregue: </strong>' + atleta["Data_Entregue"] + '</p>';
    }
    modalContent += '</pre>';

    // CLEAR THE MODAL
    $("#atletaModal").find(".modal-body").children().remove();

    $("#atletaModal").find(".modal-body").append(modalContent);

    $("#atletaModal").modal("show");
  }); // $.getJSON

} // exibeDetalhesAtleta


var putJSONOnTheTable = function(data) {
  
  /*$("#totalKits").find("small").remove();
  $("#totalKits").append('<small class="text-muted"> (' + data["KitsNaoEntregues"] + ')</small>');*/
  document.getElementById("totalKits").innerHTML = '<small class="text-muted"> (' + data["KitsNaoEntregues"] + ')</small>';  
  
  //dataResponse = JSON.parse(data);
  var atletas = data["Items"];
  if (atletas == undefined)
    return;

  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");
  table.setAttribute("class","table");

  // TABLE ROW.
  var tr = table.insertRow(-1);
  var col = ["#","Atleta","Camiseta","Camiseta Kids"];

  // TABLE HEADER.
  for (var i = 0; i < col.length; i++) {
    var th = document.createElement("th");
    th.innerHTML = col[i];
    tr.appendChild(th);
  }

  // JSON KEYS.
  var keys = ["Nome_Completo","CAMISETA","CAMISETA_KIDS"];

  // TABLE ROWS.
  for (var i = 0; i < atletas.length; i++) {

    // NEW ROW.
    tr = table.insertRow(-1);
    
    // ADD THE HIDDEN ID.
    tr.setAttribute("id", atletas[i]["Numero_de_inscricao"]);
    
    // CHECKBOX.
    var checkbox = document.createElement("input");
    checkbox.setAttribute("type","checkbox");
    var td = document.createElement("td");
    td.append(checkbox);
    tr.appendChild(td);

    // ADD THE JSON DATA TO THE TABLE AS ROWS.
    for (var j = 0; j < keys.length; j++) {
      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = atletas[i][keys[j]];
    }
  }

  var divTable = document.getElementById("div-table");
  divTable.innerHTML = "";
  divTable.appendChild(table);
  
  

} //putJSONOnTheTable



var updateTotalGroupLetters = function(groupElement, totalSelecionado) {
  
  var titleNames = {
    ad: "A - D",
    eh: "E - H",
    il: "I - L",
    mp: "M - P",
    qt: "Q - T",
    uz: "U - Z"
  }
  var title = titleNames[groupElement.attr("id").replace("link-group-","")];
  
  // Retira a quantidade da lateral dos demais grupos.
  for (var i in titleNames){
    document.getElementById("link-group-" + i).innerHTML = titleNames[i];
  }
  
  
  // Update the total deste grupo.
  /*groupElement.html(title + ' <small class="text-muted">(' + totalSelecionado + ')</small>');*/
  groupElement.html(title + ' <span class="badge">' + totalSelecionado + '</span>');
} // updateTotalGroupLetters





var shaddowThisMenu = function(currentElement) {
  
  var titleNames = {
    ad: "A - D",
    eh: "E - H",
    il: "I - L",
    mp: "M - P",
    qt: "Q - T",
    uz: "U - Z"
  }
  
  // Retira a sombra que paira sobre os menus.
  for (var i in titleNames){
    $(document.getElementById("link-group-" + i).parentElement).removeClass("active");
  }
  
  // Coloca a sombra sobre o menu selecionado.
  currentElement.parent().addClass("active");
  
  
}

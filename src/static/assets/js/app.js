//糖度
var counter = 0
document.getElementById("add_sugar").onclick = function () {

  var newSugar_size = document.getElementById("newSugar_size");

  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let td_name = document.createElement('td');
  let td_price = document.createElement('td');
  let div_name = document.createElement('div')
  let div_price = document.createElement('div')
  let div_btn = document.createElement('div')

  var plus_name = document.createElement("input");
  plus_name.type = "text";
  plus_name.name = "name";
  plus_name.placeholder = "請輸入名稱";
  plus_name.style.cssText = 'position:absolute;left:253px;';
  plus_name.setAttribute("required", "");


  var plus_price = document.createElement("input");
  plus_price.type = "text";
  plus_price.name = "price";
  plus_price.style.cssText = 'position:absolute;left:491px;';
  plus_price.placeholder = "請輸入價格";
  plus_price.setAttribute("required", "");

  let btn_delete = document.createElement('input')
  btn_delete.type = "button"
  btn_delete.value = "移除"
  btn_delete.setAttribute('class', 'btn btn-danger');
  btn_delete.style.cssText = "padding: 3px 5px; position:absolute;left:30px;"


  div_name.appendChild(plus_name)
  td_name.appendChild(div_name);
  div_price.appendChild(plus_price)
  td_price.appendChild(div_price);
  div_btn.appendChild(btn_delete)
  td.appendChild(div_btn)

  tr.appendChild(td)
  tr.appendChild(td_name);
  tr.appendChild(td_price);

  tr.id = counter
  newSugar_size.appendChild(tr)
  counter++

  btn_delete.onclick = function () {
    tr.remove()
  };

}
//冰度
document.getElementById("add_ice").onclick = function () {

  var newIce_size = document.getElementById("newIce_size");


  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let td_name = document.createElement('td');
  let td_price = document.createElement('td');
  let div_name = document.createElement('div')
  let div_price = document.createElement('div')
  let div_btn = document.createElement('div')


  var plus_name = document.createElement("input");
  plus_name.type = "text";
  plus_name.name = "name";
  plus_name.placeholder = "請輸入名稱";
  plus_name.style.cssText = 'position:absolute;left:253px;';
  plus_name.setAttribute("required", "");


  var plus_price = document.createElement("input");
  plus_price.type = "text";
  plus_price.name = "price";
  plus_price.style.cssText = 'position:absolute;left:491px;';
  plus_price.placeholder = "請輸入價格";
  plus_price.setAttribute("required", "");

  let btn_delete = document.createElement('input')
  btn_delete.type = "button"
  btn_delete.value = "移除"
  btn_delete.setAttribute('class', 'btn btn-danger');
  btn_delete.style.cssText = "padding: 3px 5px; position:absolute;left:30px;"

  div_name.appendChild(plus_name)
  td_name.appendChild(div_name);
  div_price.appendChild(plus_price)
  td_price.appendChild(div_price);
  div_btn.appendChild(btn_delete)
  td.appendChild(div_btn)


  tr.appendChild(td)
  tr.appendChild(td_name);
  tr.appendChild(td_price);
  newIce_size.appendChild(tr)
  tr.id = counter
  newIce_size.appendChild(tr)
  counter++

  btn_delete.onclick = function () {
    tr.remove()
  };

}
//咖啡加料
document.getElementById("add_coffeeplus").onclick = function () {

  var newCoffeePlus_size = document.getElementById("newCoffeePlus_size");


  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let td_name = document.createElement('td');
  let td_price = document.createElement('td');
  let div_name = document.createElement('div')
  let div_price = document.createElement('div')
  let div_btn = document.createElement('div')

  var plus_name = document.createElement("input");
  plus_name.type = "text";
  plus_name.name = "name";
  plus_name.placeholder = "請輸入名稱";
  plus_name.style.cssText = 'position:absolute;left:253px;';
  plus_name.setAttribute("required", "");


  var plus_price = document.createElement("input");
  plus_price.type = "text";
  plus_price.name = "price";
  plus_price.style.cssText = 'position:absolute;left:491px;';
  plus_price.placeholder = "請輸入價格";
  plus_price.setAttribute("required", "");

  let btn_delete = document.createElement('input')
  btn_delete.type = "button"
  btn_delete.value = "移除"
  btn_delete.setAttribute('class', 'btn btn-danger');
  btn_delete.style.cssText = "padding: 3px 5px; position:absolute;left:30px;"

  div_name.appendChild(plus_name)
  td_name.appendChild(div_name);
  div_price.appendChild(plus_price)
  td_price.appendChild(div_price);
  div_btn.appendChild(btn_delete)
  td.appendChild(div_btn)

  tr.appendChild(td)
  tr.appendChild(td_name);
  tr.appendChild(td_price);
  newCoffeePlus_size.appendChild(tr)
  tr.id = counter
  newCoffeePlus_size.appendChild(tr)
  counter++

  btn_delete.onclick = function () {
    tr.remove()
  };


}
//加料
document.getElementById("add_plus").onclick = function () {

  var newPlus_size = document.getElementById("newPlus_size");


  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let td_name = document.createElement('td');
  let td_price = document.createElement('td');
  let div_name = document.createElement('div')
  let div_price = document.createElement('div')
  let div_btn = document.createElement('div')

  var plus_name = document.createElement("input");
  plus_name.type = "text";
  plus_name.name = "name";
  plus_name.placeholder = "請輸入名稱";
  plus_name.style.cssText = 'position:absolute;left:253px;';
  plus_name.setAttribute("required", "");


  var plus_price = document.createElement("input");
  plus_price.type = "text";
  plus_price.name = "price";
  plus_price.style.cssText = 'position:absolute;left:491px;';
  plus_price.placeholder = "請輸入價格";
  plus_price.setAttribute("required", "");

  var plus_price = document.createElement("input");
  plus_price.type = "text";
  plus_price.name = "price";
  plus_price.style.cssText = 'position:absolute;left:491px;';
  plus_price.placeholder = "請輸入價格";
  plus_price.setAttribute("required", "");

  let btn_delete = document.createElement('input')
  btn_delete.type = "button"
  btn_delete.value = "移除"
  btn_delete.setAttribute('class', 'btn btn-danger');
  btn_delete.style.cssText = "padding: 3px 5px; position:absolute;left:30px;"

  div_name.appendChild(plus_name)
  td_name.appendChild(div_name);
  div_price.appendChild(plus_price)
  td_price.appendChild(div_price);
  div_btn.appendChild(btn_delete)
  td.appendChild(div_btn)

  tr.appendChild(td)
  tr.appendChild(td_name);
  tr.appendChild(td_price);
  newPlus_size.appendChild(tr)
  tr.id = counter
  newPlus_size.appendChild(tr)
  counter++

  btn_delete.onclick = function () {
    tr.remove()
  };


}
//商品類別 
document.getElementById("add_sort").onclick = function () {

  var newProductType_size = document.getElementById("newProductType_size");


  let tr = document.createElement('tr');
  let td = document.createElement('td');
  let td_name = document.createElement('td');
  let div_name = document.createElement('div')
  let div_btn = document.createElement('div')

  var plus_name = document.createElement("input");
  plus_name.type = "text";
  plus_name.name = "name";
  plus_name.placeholder = "請輸入名稱";
  plus_name.style.cssText = 'position:absolute;left:356px;';
  plus_name.setAttribute("required", "");

  let btn_delete = document.createElement('input')
  btn_delete.type = "button"
  btn_delete.value = "移除"
  btn_delete.setAttribute('class', 'btn btn-danger');
  btn_delete.style.cssText = "padding: 3px 5px; position:absolute;left:30px;"


  div_name.appendChild(plus_name)
  td_name.appendChild(div_name);
  div_btn.appendChild(btn_delete)
  td.appendChild(div_btn)

  tr.appendChild(td)
  tr.appendChild(td_name);
  newProductType_size.appendChild(tr)
  tr.id = counter
  newProductType_size.appendChild(tr)
  counter++

  btn_delete.onclick = function () {
    tr.remove()
  };
}


function cambiar_login() {
  document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";
  document.querySelector('.cont_form_login').style.display = "block";
  document.querySelector('.cont_form_sign_up').style.opacity = "0";

  setTimeout(function () { document.querySelector('.cont_form_login').style.opacity = "1"; }, 400);

  setTimeout(function () {
    document.querySelector('.cont_form_sign_up').style.display = "none";
  }, 200);
}


function ocultar_login_sign_up() {

  document.querySelector('.cont_forms').className = "cont_forms";
  document.querySelector('.cont_form_sign_up').style.opacity = "0";
  document.querySelector('.cont_form_login').style.opacity = "0";

  setTimeout(function () {
    document.querySelector('.cont_form_sign_up').style.display = "none";
    document.querySelector('.cont_form_login').style.display = "none";
  }, 500);

}


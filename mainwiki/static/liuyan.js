var btn = document.querySelector('button.sub');
var text = document.querySelector('#textarea');
var nameInput = document.querySelector('#nameInput');
var ul = document.querySelector('.article ul');
btn.onclick = function() {
  if (text.value === '' ) {
    alert('你没有输入内容，不能进行此操作');
    return false;
  } else {
    var li = document.createElement('li');
    var date = new Date();
    var dateString = date.toLocaleString();
    li.innerHTML = '</span><span class="date">' + dateString + '</span><br><span class="message">' + text.value + '</span>';
    var button = document.createElement('button');
    button.className = 'remove';
    button.innerHTML = '消除记录';
    button.onclick = function() {
      ul.removeChild(this.parentNode);
    };
    li.appendChild(button);
    ul.appendChild(li);
    text.value = '';
    nameInput.value = '';
  }
};
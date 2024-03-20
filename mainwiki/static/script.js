// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

// 这一段是我自己加的
    var btn = document.querySelector('button.sub');
    var text = document.querySelector('#textarea');
    var nameInput = document.querySelector('#nameInput');
    var ul = document.querySelector('ultalk');
    btn.onclick = function() {
        if (text.value === '' || nameInput.value === '') {
          alert('你没有输入内容或昵称，不能进行此操作');
          return false;
        } else {
          var li = document.createElement('li');
          var date = new Date();
          var dateString = date.toLocaleString();
          li.innerHTML = '<span class="name">' + nameInput.value + '</span><span class="date">' + dateString + '</span><br><span class="message">' + text.value + '</span>';
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
// 到这里为止







    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());





// Place any jQuery/helper plugins in here.

$(document).ready(function(){
	$(".contentsPanel").each(function() {
		$(this).prepend('<div class="hidePanel">[hide]</div><div class="showPanel">[show]</div>');
	});


    $(".hidePanel").click(function() {
		$( this ).siblings('ul').hide( 150, function() {
			$(this).parent().addClass('minimizedPanel');
		});
    });
    $(".showPanel").click(function() {
		$( this ).siblings('ul').show( 150, function() {
			$(this).parent().removeClass('minimizedPanel');
		});
    });
});



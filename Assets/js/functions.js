var _a = 'operator.php';
$(document).ready(function(){
    $c_t = i(p(_a,'c_t'), 'c_t');
    $s_t = i(p(_a,'s_t'), 's_t');
    $p_t = i(p(_a,'p_t'), 'p_t');

    function p(k,_p)
    {
        var _c =  $.ajax({
            url:k, type:"POST", data:_p, cache:false, async:false,success:function(_r)
            {
                console.log(_r);
            },
        }).responseText;
        return _c;
    }
    function i(_i,_t)
    {
        _t = $("#"+_t);
        _i = parseInt(_i);
        
        $({ countNum: _t.text()}).animate({
            countNum: _i
          },
        
          {
        
            duration: 8000,
            easing:'linear',
            step: function() {
                _t.text(Math.floor(this.countNum));
            },
            complete: function() {
              _t.text(this.countNum);
              //alert('finished');
            }
        
          });
        
    }
});
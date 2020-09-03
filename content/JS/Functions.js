const { extend } = require("jquery");
const electron = require('electron')
const renderer = electron.ipcRenderer;
var total_offers = 0;
var total_stores = 0;
var stores_stack = []
renderer.on('pack',(event,data) => {
    console.log(data);
    var link = data[0]; var store = data[1]; var category = data[2]; var img = data[3].replace("/content",""); var id = (Date.now() % 1000) / 1000;
    id = id.toString().replace(".","");
    $html.LoadItems(link,store,category,img,id);
    total_offers +=1;
    if(stores_stack.includes(store)=== false)
    {
        stores_stack.push(store)
        total_stores+=1;
        $desktop.DisplayTotlStores(total_stores);
    }
    $desktop.DisplayTotlOffers(total_offers);
});
class Network
{
    Get(url)
    {
        var content =  $.ajax({
            url:url, type:"GET",  cache:false, async:false,success:function(result)
            {
                console.log(result)
            },
        }).responseText;
        return content;
    }
    Post(addr,param)
    {
        var content =  $.ajax({
            url:addr, type:"POST", data:param, cache:false, async:false,success:function(result)
            {
                
            },
        }).responseText;
        return content;
    }
}
class Desktop 
{
     Board()
     {
        return $('#Board');
     }
     TotalOffers()
     {
        return $("#offers_total");
     }
     TotalStores()
     {
        return $("#stores_total");
     }
     DisplayTotlOffers(count)
     {
        this.TotalOffers().html(count);
     }
     DisplayTotlStores(count)
     {
        this.TotalStores().html(count);
     }

}
class HTML extends Network
{
    replaceAll(string, search, replace) 
    {
        return string.split(search).join(replace);
    }
    LoadItems(link,store,category,img,id)
    {
        var $output =  this.Get('../HTML/Item.html')
        $output = $output.replace('ID++;',id);
        $output = $output.replace('IMG++;',img);
        $output = $output.replace('CATEGORY++;',category);
        $output = this.replaceAll($output, "STORE++;",store);
        $output = $output.replace('LINK++;',link);

        for(var a of stack)
        {
            var nodes = new vis.DataSet([
                {id: a+1, label:  store+' '+a.toString()},
                {id: a+2, label: 'Node '+a.toString()},
                {id: a+3, label: 'Node '+a.toString()},
                {id: a+4, label: 'Node '+a.toString()},
                {id: a+5, label: 'Node '+a.toString()},
              ]);
             // create an array with edges
            var edges = new vis.DataSet([
                {from: a+1, to: 3},
                {from: a+1, to: 2},
                {from: a+2, to: 4},
                {from: a+2, to: 5},
                {from:a+3, to: 3}
            ]);
             
        }
         
        
          // create a network
          var container = document.getElementById('Board');
          var data = {
            nodes: nodes,
            edges: edges
          };
          var options = {};
          var network = new vis.Network(container, data, options);
        $desktop.Board().append($output);
        
    }
   
}

$desktop = new Desktop();
$html = new HTML();
stack = []; 
 
for($i=0; $i<20; $i++)
{
    $html.LoadItems("https://google.com","Market","CARS","https://visjs.org/images/visjs_logo.png");
    stack.push($i);
  
}
var modal = $('.modal');
var header = $(".modal > .modal-content>.modal-header>h2");
function showMore(id,event)
{    
    $target = $("#"+id);
    $category = $target.attr('category');
    modal.css('display','none');
    modal.slideDown('slow');
    $content = '<div  class="itemBox" id="'+id+'">'+$target.html() +' </div>';
    $("#preview").html($content);
    header.html($category);

    $target.toggleClass('active');
    
     
}

$('.close').click(function(){
    modal.css('display','none');
});
// create an array with nodes
 
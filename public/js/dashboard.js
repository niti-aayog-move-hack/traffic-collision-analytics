
value1 = Math.min(80, Math.max(10 + Math.round(Math.random(2)*100), 40));

var data = [ {name: "Positive", value: value1},
      {name: "Negative", value:  100-value1} ];

draw_pie("sentiment-pie", true, false, data);


function populate_words(wordarray){
  document.getElementById('wordDialog').innerHTML = wordarray.map(function(word) {
            return '<button class = "side-btn t30word" onclick = redraw_word("' + word + '","true") >'+ word +'</button>';
    }).join('');


}


function getIntro(){
      var introdata = {name : pol_name};
    $.post("/demo/intro", {data: JSON.stringify(introdata)} ,function(introduction, status){
        document.getElementById("pol-intro").innerHTML = introduction;
    });
}

getIntro();
$(window).load(function() {
    setTimeout(function() {
      /*Make the navbar normal, ie. NOT fixed for the viz*/
      $("#navbar").attr('class', 'navbar navbar-default');

      /* JS HACK to make the layer same height as intro*/

      layercake = $("#introduction").outerHeight(true);
      layercake += 130;

      $("#intro-layer").height(layercake);
      layercake = $("#intro-layer").css('height');
      console.log(layercake);
      /*Dialog box for top30 and Issues*/
    }, 0.1);
});


$("#analyze-word").add(".t30word").on("click", function() {
  $("body").toggleClass("dialogIsOpen");
})

$("#analyze-issue").add(".iss").on("click", function() {
  $("body").toggleClass("issueDialogIsOpen");
})

function toggledialog(){
  $("body").toggleClass("dialogIsOpen");
}

function toggleissuedialog(){
  $("body").toggleClass("issueDialogIsOpen");
}

/*Top 30*/

function redraw(){
  document.getElementById("wordheading").innerHTML = "What "+pol_name+" talks about: ";
  document.getElementById("analyze-word").style.display = "block";
  document.getElementById("showall").style.display = "none";
  document.getElementById("sentiment").style.display = "block";
  drawTop30('top30');

  document.getElementById('sentiment').onclick = function(){ drawTop30('top30', false, true); };
}

function redraw_word(name, resize){
  document.getElementById("wordheading").innerHTML = "What "+pol_name+" talks about: " + "<strong>" + name + "</strong>";
  document.getElementById("sentiment").style.display = "none";
  document.getElementById("showall").style.display = "block";
  document.getElementById("showall").style.marginTop = "10px";
  toggledialog();
  drawTop30(name, resize);
}


/*Issues*/

function redraw_i(){
  document.getElementById("issue_heading").innerHTML = "Issues "+pol_name+" covers: ";
  drawIssues("issues");
  document.getElementById("analyze-issue").style.display = "block";
  document.getElementById("showall_issue").style.display = "none";
  document.getElementById("sentiment_issue").style.display = "block";

  document.getElementById('sentiment_issue').onclick = function(){ drawIssues('issues', false, true); };

}

function redraw_issue(name, resize){
  document.getElementById("issue_heading").innerHTML = "What "+pol_name+" talks about: " + "<strong>" + name + "</strong>";
  document.getElementById("sentiment_issue").style.display = "none";
  document.getElementById("showall_issue").style.display = "block";
  document.getElementById("showall_issue").style.marginTop = "10px";

  drawIssues(name, resize);
}

/*Map*/

function mapsentimentwrapper(issenti){
  if(issenti){
    document.getElementById("sentiment_map").style.display = "none";
    document.getElementById("showall_map").style.display = "block";
  }
  else{
    document.getElementById("sentiment_map").style.display = "block";
    document.getElementById("showall_map").style.display = "none";
  }
  sentimap(!issenti);
}


/*CUSTOM*/

function toggleCustom(pre, res){

  document.getElementById(pre).style.display = "none";
  document.getElementById(res).style.display = "block";

}

/*WordInsights*/
function srch(){

  var q = document.getElementById("search").value;
  var searchdata = {name : pol_name, query: q};

  if(q){
        toggleCustom("pre-search", "load-search");

    $.post("/demo/search", {data: JSON.stringify(searchdata)} ,function(insights, status){

        if(!insights[0].no_result){

          toggleCustom("load-search", "res-search");
          document.getElementById("search-query").innerHTML = "Word : <strong>" + q+ "</strong>";
          document.getElementById("search-mentions").innerHTML = "<strong>" + insights[0].mentions+ "</strong>";
          document.getElementById("search-frequency").innerHTML = "<strong>" + Math.round(100*insights[0].mentions/getAvg())/100 + "</strong>";
          pie_data = [];
          common_denominator = insights[0].pos + insights[0].neg;

          positive_value = parseInt((insights[0].pos/common_denominator)*100);
          negative_value = 100 - positive_value;
  
          pie_data.push({name: "Positive", value: positive_value});
          pie_data.push({name: "Negative", value: negative_value});

          draw_pie("search-pie", true, false, pie_data);
        }

        else{
          toggleCustom("load-search", "fail-search");
        }
    });
  
  }

  else{
     document.getElementById("search-error").innerHTML = "Please enter a <strong>word</strong> for search.";
  }
}

function wrdassn(){

  var q1 = document.getElementById("w1").value;
  var q2 = document.getElementById("w2").value;

  var associationdata = {name : pol_name, OneWord: q1, TwoWord: q2};


  if(q1 && q2){
        toggleCustom("pre-association", "load-association");

    $.post("/demo/word_association", {data: JSON.stringify(associationdata)} ,function(insights, status){
       
      if(!insights[0].no_result){
        console.log(insights);
        toggleCustom("load-association", "res-association");
        document.getElementById("word-one").innerHTML = "Word : <strong>" + q1+ "</strong>";
        document.getElementById("word-two").innerHTML = "Word : <strong>" + q2+ "</strong>";
        document.getElementById("association-frequency").innerHTML = " <strong>" + insights[0].associated_mentions+ "</strong>";

        document.getElementById("word-one-heading").innerHTML = "Association from<strong> " + q1 + " </strong>to<strong> "+q2 + " </strong>";
        document.getElementById("word-two-heading").innerHTML = "Association from<strong> " + q2 + " </strong>to<strong> "+q1 + " </strong>";
        one_pie_data = [];
        two_pie_data = [];
          
        one_pie_data.push({name: "", value: insights[0].percassoc1});
        one_pie_data.push({name: "", value: 100 -insights[0].percassoc1});
        two_pie_data.push({name: "", value: insights[0].percassoc2});
        two_pie_data.push({name: "", value: 100- insights[0].percassoc2});


        draw_pie("association-one-pie", true, true, one_pie_data);
        draw_pie("association-two-pie", true, true, two_pie_data);
      }

      else{
        
      } 
  });
 }
  else{
    if(q1.length){
               document.getElementById("association-error").innerHTML = "Please enter the <strong>second word</strong> to find association.";
        }
        else if(q2.length){
               document.getElementById("association-error").innerHTML = "Please enter the <strong>first word</strong> to find association.";
        }
        else{
               document.getElementById("association-error").innerHTML = "Please enter the <strong> two words</strong> to find association.";

        }
  }

}

function prdct(){

  var q = document.getElementById("predict").value;
  var predictdata = {name : pol_name, query: q};

  if(q){
    
    toggleCustom("pre-predict", "load-predict")

    $.post("/demo/predict", {data: JSON.stringify(predictdata)} ,function(insights, status){
      
      if(!insights[0].no_result){
        
        var predict_pie_data = [];

        common_denominator = insights[0].pos + insights[0].neg;

        positive_value = parseInt((insights[0].pos/common_denominator)*100)
        negative_value = 100 - positive_value;

        predict_pie_data.push({name: "POSITIVE", value: positive_value});
        predict_pie_data.push({name: "NEGATIVE", value: negative_value});
        denom = getAvg();

        toggleCustom("load-predict", "res-predict");
        document.getElementById("predict-query").innerHTML =  q;
        document.getElementById("predict-likelyhood").innerHTML = "77%";
        draw_pie("predict-pie", true, false, predict_pie_data);
      }
      else{
          toggleCustom("load-predict", "fail-predict");
        }
    });
  }
  else{
         document.getElementById("predict-error").innerHTML = "Please enter a <strong> sentence</strong>.";
  }
}

jQuery(document).ready(function($){
  var secondaryNav = $('.cd-secondary-nav'),
    secondaryNavTopPosition = secondaryNav.offset().top,
    contentSections = $('.cd-section');

  $(window).on('scroll', function(){

    //on desktop - fix secondary navigation on scrolling
    if($(window).scrollTop() > secondaryNavTopPosition ) {
      //fix secondary navigation
      secondaryNav.addClass('is-fixed');
      //push the .cd-main-content giving it a top-margin
      $('.cd-main-content').addClass('has-top-margin');
      //on Firefox CSS transition/animation fails when parent element changes position attribute
      //so we to change secondary navigation childrens attributes after having changed its position value
      setTimeout(function() {
              secondaryNav.addClass('animate-children');
              $('#cd-logo').addClass('slide-in');
          }, 50);
    } else {
      secondaryNav.removeClass('is-fixed');
      $('.cd-main-content').removeClass('has-top-margin');
      setTimeout(function() {
              secondaryNav.removeClass('animate-children');
              $('#cd-logo').removeClass('slide-in');
          }, 50);
    }

    //on desktop - update the active link in the secondary fixed navigation
    updateSecondaryNavigation();
  });

  function updateSecondaryNavigation() {
    contentSections.each(function(){
      var actual = $(this),
        actualHeight = actual.height() + parseInt(actual.css('paddingTop').replace('px', '')) + parseInt(actual.css('paddingBottom').replace('px', '')),
        actualAnchor = secondaryNav.find('a[href="#'+actual.attr('id')+'"]');
      if ( ( actual.offset().top - secondaryNav.height() <= $(window).scrollTop() ) && ( actual.offset().top +  actualHeight - secondaryNav.height() > $(window).scrollTop() ) ) {
        actualAnchor.addClass('active');
      }else {
        actualAnchor.removeClass('active');
      }
    });
  }

  //on mobile - open/close secondary navigation clicking/tapping the .cd-secondary-nav-trigger
  $('.cd-secondary-nav-trigger').on('click', function(event){
    event.preventDefault();
    $(this).toggleClass('menu-is-open');
    secondaryNav.find('ul').toggleClass('is-visible');
  });

  //smooth scrolling when clicking on the secondary navigation items
  secondaryNav.find('ul a').on('click', function(event){
        event.preventDefault();
        var target= $(this.hash);
        $('body,html').animate({
          'scrollTop': target.offset().top - secondaryNav.height() + 1
          }, 400
        ); 
        //on mobile - close secondary navigation
        $('.cd-secondary-nav-trigger').removeClass('menu-is-open');
        secondaryNav.find('ul').removeClass('is-visible');
    });

    //on mobile - open/close primary navigation clicking/tapping the menu icon
  $('.cd-primary-nav').on('click', function(event){
    if($(event.target).is('.cd-primary-nav')) $(this).children('ul').toggleClass('is-visible');
  });
});
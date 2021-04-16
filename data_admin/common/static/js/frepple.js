// Django sets this variable in the admin/base.html template.
window.__admin_media_prefix__ = "/static/admin/";

//check for browser features
function isDragnDropUploadCapable() {
  var adiv = document.createElement('div');
  return (('draggable' in adiv) || ('ondragstart' in adiv && 'ondrop' in adiv)) && 'FormData' in window && 'FileReader' in window;
}

var _scrollBarWidth;
function getScrollBarWidth() {
  if (!_scrollBarWidth) {
    var div = $("<div style='overflow:scroll;position:absolute;top:-99999px'></div>").appendTo("body"),
    _scrollBarWidth = div.prop("offsetWidth") - div.prop("clientWidth");
    div.remove();
  }
  return _scrollBarWidth;
}


// Adjust the breadcrumbs such that it fits on a single line.
// This function is called when the window is resized.
function breadcrumbs_reflow()
{
  var crumbs = $("#breadcrumbs");
  var height_one_line = Math.ceil($("#cockpitcrumb").height()) + 16;

  // Show all elements previously hidden
  crumbs.children("li:hidden").show();
  // Hide the first crumbs till it all fits on a single line.
  var first = true;
  crumbs.children("li").each(function() {
    if (crumbs.height() > height_one_line && !first) $(this).hide();
    first = false;
  });
}


// A function to escape all special characters in a name.
// We escape all special characters in the EXACT same way as the django admin does.
function admin_escape(n)
{
  if (!n) return "";
  return n.replace(/_/g,'_5F')
  .replace(/:/g,'_3A').replace(/\//g,'_2F').replace(/#/g,'_23').replace(/\?/g,'_3F')
  .replace(/;/g,'_3B').replace(/@/g,'_40').replace(/&/g,'_26').replace(/=/g,'_3D')
  .replace(/\+/g,'_2B').replace(/\$/g,'_24').replace(/,/g,'_2C').replace(/"/g,'_22')
  .replace(/</g,'_3C').replace(/>/g,'_3E').replace(/%/g,'_25').replace(/\\/g,'_5C')
  .replace(/\t/g,'%09');
}


// A function to unescape all special characters in a name.
// We unescape all special characters in the EXACT same way as the django admin does.
function admin_unescape(n)
{
  return n.replace(/_5F/g,'_')
  .replace(/_3A/g,':').replace(/_2F/g,'/').replace(/_23/g,'#').replace(/_3F/g,'?')
  .replace(/_3B/g,';').replace(/_40/g,'@').replace(/_26/g,'&').replace(/_3D/g,'=')
  .replace(/_2B/g,'+').replace(/_24/g,'$').replace(/_2C/g,',').replace(/_22/g,'"')
  .replace(/_3C/g,'<').replace(/_3E/g,'>').replace(/_25/g,'%').replace(/_5C/g,'\\');
}


/// <reference path="jquery.js" />
/*
jquery-resizable
Version 0.14 - 1/4/2015
© 2015 Rick Strahl, West Wind Technologies
www.west-wind.com
Licensed under MIT License
*/

    $.fn.resizable = function fnResizable(options) {
        var opt = {
            // selector for handle that starts dragging
            handleSelector: null,
            // resize the width
            resizeWidth: true,
            // resize the height
            resizeHeight: true,
            // hook into start drag operation (event passed)
            onDragStart: null,
            // hook into stop drag operation (event passed)
            onDragEnd: null,
            // hook into each drag operation (event passed)
            onDrag: null,
            // disable touch-action on $handle
            // prevents browser level actions like forward back gestures
            touchActionNone: true
        };
        if (typeof options == "object") opt = $.extend(opt, options);

        return this.each(function () {
            var startPos, startTransition;

            var $el = $(this);
            if ($(this).hasClass("ui-jqgrid")) return; //fix for Firefox bug that adds resize to the grid, we want only to resize the grid parent div ex: "content-main"

            var $handle = opt.handleSelector ? $(opt.handleSelector) : $el;

            if (opt.touchActionNone)
                $handle.css("touch-action", "none");

            $el.addClass("resizable");
            $handle.bind('mousedown.rsz touchstart.rsz', startDragging);

            function noop(e) {
                e.stopPropagation();
                e.preventDefault();
            };

            function startDragging(e) {
                startPos = getMousePos(e);
                startPos.width = parseInt($el.width(), 10);
                startPos.height = parseInt($el.height(), 10);

                startTransition = $el.css("transition");
                $el.css("transition", "none");

                if (opt.onDragStart) {
                    if (opt.onDragStart(e, $el, opt) === false)
                        return;
                }
                opt.dragFunc = doDrag;

                $(document).bind('mousemove.rsz', opt.dragFunc);
                $(document).bind('mouseup.rsz', stopDragging);
                if (window.Touch || navigator.maxTouchPoints) {
                    $(document).bind('touchmove.rsz', opt.dragFunc);
                    $(document).bind('touchend.rsz', stopDragging);
                }
                $(document).bind('selectstart.rsz', noop); // disable selection
            }

            function doDrag(e) {
                var pos = getMousePos(e);

                if (opt.resizeWidth) {
                    var newWidth = startPos.width + pos.x - startPos.x;
                    $el.width(newWidth);
                }

                if (opt.resizeHeight) {
                    var newHeight = startPos.height + pos.y - startPos.y;
                    $el.height(newHeight);
                }

                if (opt.onDrag)
                    opt.onDrag(e, $el, opt);
            }

            function stopDragging(e) {
                e.stopPropagation();
                e.preventDefault();

                $(document).unbind('mousemove.rsz', opt.dragFunc);
                $(document).unbind('mouseup.rsz', stopDragging);

                if (window.Touch || navigator.maxTouchPoints) {
                    $(document).unbind('touchmove.rsz', opt.dragFunc);
                    $(document).unbind('touchend.rsz', stopDragging);
                }
                $(document).unbind('selectstart.rsz', noop);

                // reset changed values
                $el.css("transition", startTransition);

                if (opt.onDragEnd)
                    opt.onDragEnd(e, $el, opt);

                return false;
            }

            function getMousePos(e) {
                var pos = { x: 0, y: 0, width: 0, height: 0 };
                if (typeof e.clientX === "number") {
                    pos.x = e.clientX;
                    pos.y = e.clientY;
                } else if (e.originalEvent.touches) {
                    pos.x = e.originalEvent.touches[0].clientX;
                    pos.y = e.originalEvent.touches[0].clientY;
                } else
                    return null;

                return pos;
            }
        });
    }
// end of jquery-resizable copy


function ajaxerror(result, stat, errorThrown) {
  var msg;
  if (result.readyState == 0)
    // Network errors: network down, server down, access denied...
    msg = gettext("Connection failed");
  else if (errorThrown)
    msg = "<strong>" + errorThrown + "</strong><br>" + result.responseText;
  else
    msg = result.responseText;
  $('#timebuckets').modal('hide');
  $.jgrid.hideModal("#searchmodfbox_grid");
  $('#popup').html(
    '<div class="modal-dialog">'+
    '<div class="modal-content">'+
      '<div class="modal-header bg-danger">'+
        '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
        '<h4 class="modal-title">'+ gettext("Error")+'</h4>'+
      '</div>'+
      '<div class="modal-body">'+
        '<p>' + msg + '</p>'+
      '</div>'+
      '<div class="modal-footer">'+
        '<input type="submit" role="button" class="btn btn-primary pull-right" data-dismiss="modal" value="'+gettext('Close')+'">'+
      '</div>'+
    '</div>'+
    '</div>'
    ).modal('show');
}
         
//----------------------------------------------------------------------------
// A class to handle changes to a grid.
//----------------------------------------------------------------------------
var upload = {
  warnUnsavedChanges: function()
  {
    $(window).off('beforeunload', upload.warnUnsavedChanges);
    return gettext("There are unsaved changes on this page.");
  },

  undo : function ()
  {
    if ($('#undo').hasClass("btn-primary")) return;
    if (typeof extraSearchUpdate == 'function') {
      var f = $('#grid').getGridParam("postData").filters;
  	  if (!extraSearchUpdate(f ? JSON.parse(f) : null))
  		  $("#grid").trigger("reloadGrid");
    }
    else
    	$("#grid").trigger("reloadGrid");
    $("#grid").closest(".ui-jqgrid-bdiv").scrollTop(0);
    $('#save, #undo').addClass("btn-primary").removeClass("btn-danger").prop('disabled', true);
    $('#actions1').prop('disabled', true);
    $(window).off('beforeunload', upload.warnUnsavedChanges);
  },

  select : function ()
  {
    $.jgrid.hideModal("#searchmodfbox_grid");
    $('#save, #undo').removeClass("btn-primary").addClass("btn-danger").prop('disabled', false);
    $(window).off('beforeunload', upload.warnUnsavedChanges);
    $(window).on('beforeunload', upload.warnUnsavedChanges);
  },

  selectedRows : [],
  
  restoreSelection : function() {
    grid.markSelectedRow(upload.selectedRows.length);
    for (var r in upload.selectedRows)
    	$("#grid").jqGrid('setSelection', upload.selectedRows[r], false);
    upload.selectedRows = [];  	
  },
  
  save : function()
  {
    if ($('#save').hasClass("btn-primary")) return;

    // Pick up all changed cells. If a function "getData" is defined on the
    // page we use that, otherwise we use the standard functionality of jqgrid.
    $("#grid").saveCell(editrow, editcol);
    if (typeof getDirtyData == 'function')
      var rows = getDirtyData();
    else
      var rows = $("#grid").getChangedCells('dirty');
    
    // Remember the selected rows, which will be restored in the loadcomplete event
    var tmp = $("#grid").jqGrid("getGridParam", "selarrrow");
    upload.selectedRows = tmp ? tmp.slice() : null;
    
    if (rows != null && rows.length > 0)
      // Send the update to the server
      $.ajax({
          url: location.pathname,
          data: JSON.stringify(rows),
          type: "POST",
          contentType: "application/json",
          success: function () {
            upload.undo();
            },
          error: ajaxerror
        });
  },

  validateSort: function(event)
  {
    if ($(this).attr('id') == 'grid_cb') return;
    if ($("body").hasClass("popup"))  return;
    if ($('#save').hasClass("btn-primary"))
      jQuery("#grid").jqGrid('resetSelection');
    else
    {
      $('#timebuckets').modal('hide');
      $.jgrid.hideModal("#searchmodfbox_grid");
      $('#popup').html('<div class="modal-dialog">'+
          '<div class="modal-content">'+
          '<div class="modal-header alert-warning" style="border-top-left-radius: inherit; border-top-right-radius: inherit">'+
            '<h4 class="modal-title">'+ gettext("Save or cancel your changes first") +'</h4>'+
          '</div>'+
          '<div class="modal-body">'+
            gettext("There are unsaved changes on this page.") +
          '</div>'+
          '<div class="modal-footer">'+
            '<input type="submit" id="savebutton" role="button" class="btn btn-danger pull-left" value="'+gettext('Save')+'">'+
            '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Cancel')+'">'+
          '</div>'+
        '</div>'+
      '</div>' )
      .modal('show');
      $('#savebutton').on('click', function() {
                upload.save();
        $('#popup').modal('hide');
      });
      $('#cancelbutton').on('click', function() {
                upload.undo();
        $('#popup').modal('hide');
        });
      event.stopPropagation();
    }
  }
}

//----------------------------------------------------------------------------
// Custom formatter functions for the grid cells.
//----------------------------------------------------------------------------

function opendetail(event) {
	var el = $(event.target).parent();
  var curlink = el.attr('href');
  var objectid = el.attr('objectid');
  if (objectid === undefined || objectid == false)
  	objectid = el.parent().text().trim();
  event.preventDefault();
  event.stopImmediatePropagation();
  window.location.href = url_prefix + curlink.replace('key', admin_escape(objectid));
}


function formatDuration(cellvalue, options, rowdata) {
  var days = 0;
  var hours = 0;
  var minutes =0;
  var seconds = 0;
  var sign;
  var d = [];
  var t = [];

  if (cellvalue === undefined || cellvalue === '' || cellvalue === null) return '';
  if (typeof cellvalue === "number") {
    seconds = cellvalue;
    sign = Math.sign(seconds);
  } else {
    sign = ($.trim(cellvalue).charAt(0) == '-')?-1:1;
    d = cellvalue.replace(/ +/g, " ").split(" ");
    if (d.length == 1)
    {
      t = cellvalue.split(":");
      days = 0;
    }
    else
    {
      t = d[1].split(":");
      days = (d[0]!='' ? parseFloat(d[0]) : 0);
    }
    switch (t.length)
    {
      case 0: // Days only
        seconds = Math.abs(days) * 86400;
        break;
      case 1: // Days, seconds
        seconds = Math.abs(days) * 86400 + (t[0]!='' ? Math.abs(parseFloat(t[0])) : 0);
        break;
      case 2: // Days, minutes and seconds
        seconds = Math.abs(days) * 86400 + (t[0]!='' ? Math.abs(parseFloat(t[0])) : 0) * 60 + (t[1]!='' ? parseFloat(t[1]) : 0);
        break;
      default:
        // Days, hours, minutes, seconds
        seconds = Math.abs(days) * 86400 + (t[0]!='' ? Math.abs(parseFloat(t[0])) : 0) * 3600 + (t[1]!='' ? parseFloat(t[1]) : 0) * 60 + (t[2]!='' ? parseFloat(t[2]) : 0);
    }
  }
  seconds = Math.abs(seconds); //remove the sign
  days = Math.floor(seconds / 86400);
  hours = Math.floor((seconds - (days * 86400)) / 3600);
  minutes = Math.floor((seconds - (days * 86400) - (hours * 3600)) / 60);
  seconds = seconds - (days * 86400) - (hours * 3600) - (minutes * 60);

  if (days > 365 * 5)
  	// When it's more than 5 years, we assume you meant infinite
  	return 'N/A';
  if (days > 0)
    return (sign*days).toString() 
      + " " + ((hours < 10) ? "0" : "") + hours + ((minutes < 10) ? ":0" : ":") 
      + minutes + ((seconds < 10) ? ":0" : ":") 
      + Number((seconds).toFixed((seconds === Math.floor(seconds))?0:6));
  else
    return ((sign<0)?"-":"") + ((hours < 10) ? "0" : "") + hours 
      + ((minutes < 10) ? ":0" : ":") + minutes 
      + ((seconds < 10) ? ":0" : ":") 
      + Number((seconds).toFixed((seconds === Math.floor(seconds))?0:6));
}

jQuery.extend($.fn.fmatter, {
  percentage : function(cellvalue, options, rowdata) {
    if (cellvalue === undefined || cellvalue === '' || cellvalue === null) return '';
    return grid.formatNumber(cellvalue) + "%";
  },

  duration : formatDuration,

  image : function(cellvalue, options, rowdata) {
    return cellvalue ?
      '<img class="avatar-sm" src="/uploads/' + cellvalue + '">' :
      '';
  },
  
  admin : function(cellvalue, options, rowdata) {
    if (cellvalue === undefined || cellvalue === '' || cellvalue === null)
      return '';
    if (options['colModel']['popup'] || rowdata.showdrilldown === '0')
      return $.jgrid.htmlEncode(cellvalue);
    return $.jgrid.htmlEncode(cellvalue) 
      + "<a href='" + url_prefix + "/data/" + options.colModel.role + "/" + admin_escape(cellvalue) 
      + "/change/' onclick='event.stopPropagation()'><span class='leftpadding fa fa-caret-right'></span></a>";
  },

  detail : function(cellvalue, options, rowdata) {
    if (cellvalue === undefined || cellvalue === '' || cellvalue === null)
      return '';
    if (options['colModel']['popup'])
      return $.jgrid.htmlEncode(cellvalue);
    if (options.colModel.name == "operation") {
    	if (rowdata.hasOwnProperty('type') 
    			&& (rowdata.type === 'PO' || rowdata.type === 'DO' || rowdata.type === 'DLVR' || rowdata.type === 'STCK' ))
          return $.jgrid.htmlEncode(cellvalue); //don't show links for non existing operations
      if (rowdata.hasOwnProperty('operationplan__type')
      		&& (rowdata.operationplan__type === 'PO' || rowdata.operationplan__type === 'DO' 
      			|| rowdata.operationplan__type === 'DLVR' || rowdata.operationplan__type === 'STCK' ))
          return $.jgrid.htmlEncode(cellvalue); //don't show links for non existing operations
    }    
    return $.jgrid.htmlEncode(cellvalue) 
      + "<a href=\"" + url_prefix + "/detail/" + options.colModel.role + "/" + admin_escape(cellvalue) 
      + "/\" onclick='event.stopPropagation()'><span class='leftpadding fa fa-caret-right'></span></a>";
  },

  demanddetail : function(cellvalue, options, rowdata) {
    if (cellvalue === undefined || cellvalue === '')
    	return '';
    if (options['colModel']['popup'])
    	return $.jgrid.htmlEncode(cellvalue);
    var result = '';
    var count = cellvalue.length;
    for (var i = 0; i < count; i++)
    {
      if (result != '')
      	result += ', ';
        result += cellvalue[i][0] + " : " + $.jgrid.htmlEncode(cellvalue[i][1])
          + "<a href=\"" + url_prefix + "/detail/input/demand/" + admin_escape(cellvalue[i][1])
          + "/\" onclick='event.stopPropagation()'><span class='leftpadding fa fa-caret-right' role='input/demand'></span></a>";
    }
    return result;
  },

  listdetail : function(cellvalue, options, rowdata) {
    if (cellvalue === undefined || cellvalue === '')
    	return '';
    if (options['colModel']['popup'])
    	return cellvalue;
    var result = '';
    var count = cellvalue.length;
    for (var i = 0; i < count; i++)
    {
      if (result != '')
      	result += ', ';
      result += '<span><span class="listdetailkey">' + $.jgrid.htmlEncode(cellvalue[i][0])
        + "</span><a href=\"" + url_prefix + "/detail/" + options.colModel.role 
        + "/" + admin_escape(cellvalue[i][0]) 
        + "/\" onclick='event.stopPropagation()'><span class='leftpadding fa fa-caret-right' role='" 
        + options.colModel.role + "'></span></a></span>&nbsp;<span>" + cellvalue[i][1] + "</span>";
    }
    return result;
  },

  graph : function (cellvalue, options, rowdata) {
    return '<div class="graph" style="height:80px"></div>';
  },

  longstring : function (cellvalue, options, rowdata) {
    if (typeof cellvalue !== 'string') return "";
    var tipcontent = $.jgrid.htmlEncode(cellvalue);
    return '<span data-toggle="tooltip" data-placement="left" data-original-title="'+tipcontent+'">'+tipcontent+'</span>';
  },

  selectbutton : function(cellvalue, options, rowdata) {
    if (cellvalue) 
    	return '<button onClick="opener.dismissRelatedLookupPopup(window, grid.selected)" class="btn btn-primary btn-xs">'
    	  + gettext('select')
    	  + '</button>';
    else
    	return "";
  },

  color : function (cellvalue, options, rowdata) {
      
	  if (rowdata.color === undefined || rowdata.color === '')
		  return '';
		  
	  // Ignores color field and read the delay field
      var thedelay = Math.round(parseInt(rowdata.delay)/8640)/10;
      if (parseInt(rowdata.criticality) === 999 || parseInt(rowdata.operationplan__criticality) === 999) {
        return '';
      } else if (thedelay < 0) {
        return '<div class="invStatus" style="text-align: center; background-color: #008000; color: #151515;">'+ (-thedelay)+' '+gettext("days early")+'</div>';
      } else if (thedelay === 0) {
        return '<div class="invStatus" style="text-align: center; background-color: #008000; color: #151515;">'+gettext("on time")+'</div>';
      } else if (thedelay > 0) {
        return '<div class="invStatus" style="text-align: center; background-color: #f00; color: #151515;">'+thedelay+' '+gettext("days late")+'</div>';        
      }    
    return '';
  },
  
  number: function (nData, opts) {
  	return grid.formatNumber(nData);
	}
});

jQuery.extend($.fn.fmatter.percentage, {
    unformat : function(cellvalue, options, cell) {
      return cellvalue.replace("%", "");
      }
});

jQuery.extend($.fn.fmatter.listdetail, {
	unformat: function(cellvalue, options, cell) {
		var o = [];
		$('.listdetailkey', $(cell)).each(function(idx, val) {
			o.push([$(val).text(), $(val).parent().next("span").text()]);
		});
    return o;		
	}
});


//
// Functions related to jqgrid
//

var grid = {

   // Popup row selection.
   // The popup window present a list of objects. The user clicks on a row to
   // select it and a "select" button appears. When this button is clicked the
   // popup is closed and the selected id is passed to the calling page.
   selected: undefined,

   formatNumber: function(nData, maxdecimals=6) {
  	 // Number formatting function copied from free-jqgrid.
  	 // Adapted to show a max number of decimal places.
  	 if (typeof(nData) === 'undefined')
  		 return '';
  	  var isNumber = $.fmatter.isNumber;
			if (!isNumber(nData))
				nData *= 1;
			if (isNumber(nData)) {
				var bNegative = (nData < 0);				
				var sOutput;
				if (nData > 100000 || maxdecimals <= 0)
					sOutput = String(parseFloat(nData.toFixed()));
				else if (nData > 10000 || maxdecimals <= 1)
					sOutput = String(parseFloat(nData.toFixed(1)));
				else if (nData > 1000 || maxdecimals <= 2)
					sOutput = String(parseFloat(nData.toFixed(2)));
				else if (nData > 100 || maxdecimals <= 3)
					sOutput = String(parseFloat(nData.toFixed(3)));
				else if (nData > 10 || maxdecimals <= 4)
					sOutput = String(parseFloat(nData.toFixed(4)));
				else if (nData > 1 || maxdecimals <= 5)
					sOutput = String(parseFloat(nData.toFixed(5)));
				else
					sOutput = String(parseFloat(nData.toFixed(maxdecimals)));
				var sDecimalSeparator = jQuery("#grid").jqGrid("getGridRes", "formatter.number.decimalSeparator") || ".";
				if (sDecimalSeparator !== ".") 
					// Replace the "."
					sOutput = sOutput.replace(".", sDecimalSeparator);
				var sThousandsSeparator = jQuery("#grid").jqGrid("getGridRes", "formatter.number.thousandsSeparator") || ",";
				if (sThousandsSeparator) {
					var nDotIndex = sOutput.lastIndexOf(sDecimalSeparator);
					nDotIndex = (nDotIndex > -1) ? nDotIndex : sOutput.length;
					// we cut the part after the point for integer numbers
					// it will prevent storing/restoring of wrong numbers during inline editing
					var sNewOutput = sDecimalSeparator === undefined ? "" : sOutput.substring(nDotIndex);
					var nCount = -1, i;
					for (i = nDotIndex; i > 0; i--) {
						nCount++;
						if ((nCount % 3 === 0) && (i !== nDotIndex) && (!bNegative || (i > 1))) {
							sNewOutput = sThousandsSeparator + sNewOutput;
						}
						sNewOutput = sOutput.charAt(i - 1) + sNewOutput;
					}
					sOutput = sNewOutput;
				}
				return sOutput;
			}
			return nData;
   },
   
   // Function used to summarize by returning the last value
   summary_last: function(val, name, record)
   {
     return record[name];
   },

   // Function used to summarize by returning the first value
   summary_first: function(val, name, record)
   {
     return val || record[name];
   },

   setSelectedRow: function(id)
   {
     if (grid.selected != undefined)
       $(this).jqGrid('setCell', grid.selected, 'select', null);
     grid.selected = id;
     $(this).jqGrid('setCell', id, 'select', true);
   },

   runAction: function(next_action) {
    if ($("#actions").val() != "no_action")
       actions[$("#actions").val()]();
   },

   setStatus : function(newstatus)
   {
    var sel = jQuery("#grid").jqGrid('getGridParam','selarrrow');
    for (var i in sel) {
      jQuery("#grid").jqGrid("setCell", sel[i], "status", newstatus, "dirty-cell");
      jQuery("#grid").jqGrid("setRowData", sel[i], false, "edited");
    };
    $("#actions1").html(gettext("Select action") + '&nbsp;&nbsp;<span class="caret"></span>');
    $('#save').removeClass("btn-primary").addClass("btn-danger").prop("disabled",false);
    $('#undo').removeClass("btn-primary").addClass("btn-danger").prop("disabled",false);
   },

  // Renders the cross list in a pivot grid
  pivotcolumns : function  (cellvalue, options, rowdata)
  {
    var result = '';
    for (var i of cross_idx)
    {
      if (cross[i]['editable'])
        result += '<span class="editablepivotcol">' + cross[i]['name'] + '</span>';
      else
        result += cross[i]['name'] + '<br>';
    }
    return result;
  },

  // Render the customization popup window
  showCustomize: function (pivot, gridid, cross_arg, cross_idx_arg, cross_only_arg, ok_callback, reset_callback)
  {
    $('#timebuckets').modal('hide');
    $.jgrid.hideModal("#searchmodfbox_grid");
  	var thegrid = $((typeof gridid !== 'undefined') ? gridid : "#grid");
    var colModel = thegrid.jqGrid('getGridParam', 'colModel');
    var maxfrozen = 0;
    var skipped = 0;
    var graph = false;
    var cross_only = pivot && typeof cross_only_arg !== 'undefined' && cross_only_arg;
    	
    var row0 = cross_only ?
	      '' :
	      '<div class="row">' +
	      '<div class="col-xs-6">' +
	        '<div class="panel panel-default"><div class="panel-heading">'+ gettext("Selected options") + '</div>' +
	          '<div class="panel-body">' +
	            '<ul class="list-group" id="Rows" style="height: 160px; overflow-y: scroll;">placeholder0</ul>' +
	          '</div>' +
	        '</div>'+
	      '</div>' +
	      '<div class="col-xs-6">' +
	        '<div class="panel panel-default"><div class="panel-heading">' + gettext("Available options") + '</div>' +
	          '<div class="panel-body">' +
	            '<ul class="list-group" id="DroppointRows" style="height: 160px; overflow-y: scroll;">placeholder1</ul>' +
	          '</div>' +
	        '</div>' +
	      '</div>' +
	    '</div>';

    var row1= "";
    var row2= "";

    var val0s = ""; //selected columns
    var val0a = ""; //available columns
    var val1s = ""; //selected crosses
    var val1a = ""; //available crosses

    for (var i in colModel)
    {
      if (colModel[i].name == 'graph')
        graph = true;
      else if (colModel[i].name != "rn" && colModel[i].name != "cb" && colModel[i].counter != null && colModel[i].label != '' && !('alwayshidden' in colModel[i]))
      {
        if (colModel[i].frozen) maxfrozen = parseInt(i,10) + 1 - skipped;
        if (!colModel[i].hidden) {
          val0s += '<li id="' + (i) + '"  class="list-group-item" style="cursor: move;">' + colModel[i].label + '</li>';
        } else {
          val0a += '<li id="' + (i) + '"  class="list-group-item" style="cursor: move;">' + colModel[i].label + '</li>';
        }
      }
      else
        skipped++;
    }

    if (pivot)
    {      
      var my_cross = (typeof cross_arg !== 'undefined') ? cross_arg : cross;
      var my_cross_idx = (typeof cross_idx_arg !== 'undefined') ? cross_idx_arg : cross_idx;
      // Add list of crosses
      var row1 = ''+
      '<div class="row">' +
        '<div class="col-xs-6">' +
          '<div class="panel panel-default">' +
            '<div class="panel-heading">' +
              gettext('Selected Cross') +
            '</div>' +
            '<div class="panel-body">' +
              '<ul class="list-group" id="Crosses" style="height: 160px; overflow-y: scroll;">placeholder0</ul>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="col-xs-6">' +
          '<div class="panel panel-default">' +
            '<div class="panel-heading">' +
              gettext('Available Cross') +
            '</div>' +
            '<div class="panel-body">' +
              '<ul class="list-group" id="DroppointCrosses" style="height: 160px; overflow-y: scroll;">placeholder1</ul>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';
      for (var j in my_cross_idx)
      {
        val1s += '<li class="list-group-item" id="' + (100+parseInt(my_cross_idx[j],10)) + '" style="cursor: move;">' + my_cross[my_cross_idx[j]]['name'] + '</li>';
      }
      for (var j in my_cross)
      {
        if (my_cross_idx.indexOf(parseInt(j,10)) > -1 || my_cross[j]['name'] == "") continue;
        val1a += '<li class="list-group-item" id="' + (100 + parseInt(j,10) ) + '" style="cursor: move;">' + my_cross[j]['name'] + '</li>';
      }
    }
    else
    {
      // Add selection of number of frozen columns
      row2 = '<div class="row"><div class="col-xs-12">' +
        gettext("Frozen columns") +
        '&nbsp;&nbsp;<input type="number" id="frozen" style="text-align: center;" min="0" max="4" step="1" value="' + maxfrozen + '">' +
       '</div></div>';
    }

    row0 = row0.replace('placeholder0',val0s);
    row0 = row0.replace('placeholder1',val0a);
    if (pivot) {
      row1 = row1.replace('placeholder0',val1s);
      row1 = row1.replace('placeholder1',val1a);
    }

    $('#popup').html(''+
      '<div class="modal-dialog">'+
        '<div class="modal-content">'+
          '<div class="modal-header">'+
            '<button type="button" class="close" data-dismiss="modal" aria-label=' + gettext("Close") + '>' +
              '<span aria-hidden="true" class="fa fa-times"></span>' +
            '</button>'+
            '<h4 class="modal-title">'+gettext("Customize")+'</h4>'+
          '</div>'+
          '<div class="modal-body">'+
            row0 +
            row1 +
            row2 +
          '</div>' +
          '<div class="modal-footer">'+
            '<input type="submit" id="okCustbutton" role="button" class="btn btn-primary pull-right" value="'+gettext("OK")+'">'+
            '<input type="submit" id="cancelCustbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
            '<input type="submit" id="resetCustbutton" role="button" class="btn btn-primary pull-left" value="'+gettext('Reset')+'">'+
          '</div>'+
        '</div>'+
      '</div>' )
    .modal('show');

    if (!cross_only) {
	    var Rows = document.getElementById("Rows");
	    var DroppointRows = document.getElementById("DroppointRows");
	    Sortable.create(Rows, {
	      group: {
	        name: 'Rows',
	        put: ['DroppointRows']
	      },
	      animation: 100
	    });
	    Sortable.create(DroppointRows, {
	      group: {
	        name: 'DroppointRows',
	        put: ['Rows']
	      },
	      animation: 100
	    });
    }
    
    if (pivot) {
      var Crosses = document.getElementById("Crosses");
      var DroppointCrosses = document.getElementById("DroppointCrosses");
      Sortable.create(Crosses, {
        group: {
          name: 'Crosses',
          put: ['DroppointCrosses']
        },
        animation: 100
      });
      Sortable.create(DroppointCrosses, {
        group: {
          name: 'DroppointCrosses',
          put: ['Crosses']
        },
        animation: 100
      });
    }

    $('#resetCustbutton').on(
    	'click',
    	typeof reset_callback !== 'undefined' ? reset_callback : function() {
      var result = {};
      result[reportkey] = {"favorites": favorites};
      if (typeof url_prefix != 'undefined')
        var url = url_prefix + '/settings/';
      else
        var url = '/settings/';
      $.ajax({
       url: url,
       type: 'POST',
       contentType: 'application/json; charset=utf-8',
       data: JSON.stringify(result),
       success: function() {window.location.href = window.location.href;},
       error: ajaxerror
       });
     });

    $('#okCustbutton').on(
    	'click',
    	typeof ok_callback !== 'undefined' ? ok_callback : function() {
      var colModel = $("#grid")[0].p.colModel;
      var perm = [];
      var hiddenrows = [];
      if (colModel[0].name == "cb") perm.push(0);
      cross_idx = [];
      if (!graph)
        $("#grid").jqGrid('destroyFrozenColumns');

      $('#Rows li').each(function() {
        var val = parseInt(this.id,10);
        if (val < 100)
        {
            $("#grid").jqGrid("showCol", colModel[val].name);
            perm.push(val);
         }
      });

      $('#DroppointRows li').each(function() {
        var val = parseInt(this.id,10);
        if (val < 100)
        {
          hiddenrows.push(val);
          if (pivot)
            $("#grid").jqGrid('setColProp', colModel[val].name, {frozen:false});
          $("#grid").jqGrid("hideCol", colModel[val].name);
         }
      });

      $('#Crosses li').each(function() {
        var val = parseInt(this.id,10);
        if (val >= 100)
          cross_idx.push(val-100);
      });

      var numfrozen = 0;
      if (pivot) {
        for (var i in colModel)
          if ("counter" in colModel[i])
            numfrozen = parseInt(i)+1;
          else
            perm.push(parseInt(i));
      }
      else
        numfrozen = parseInt($("#frozen").val());
      for (var i in hiddenrows)
        perm.push(hiddenrows[i]);
      for (var i in colModel)
        if ("alwayshidden" in colModel[i])
        	perm.push(parseInt(i));
      $("#grid").jqGrid("remapColumns", perm, true);
      var skipped = 0;
      for (var i in colModel)
        if (colModel[i].name != "rn" && colModel[i].name != "cb" && colModel[i].counter != null)
          $("#grid").jqGrid('setColProp', colModel[i].name, {frozen:i-skipped<numfrozen});
        else
          skipped++;
      if (!graph)
        $("#grid").jqGrid('setFrozenColumns');
      $("#grid").trigger('reloadGrid');
      grid.saveColumnConfiguration();
      $('#popup').modal("hide");
    });
  },

  getGridConfig: function() {
    // Returns the current settings of the grid:
  	// 1) Filter
  	// 2) Sorting
  	// 3) Column configuration
    var colArray = new Array();
    var colModel = $("#grid").jqGrid('getGridParam', 'colModel');
    var pivot = false;
    var skipped = 0;
    var maxfrozen = 0;
    for (var i in colModel)
    {
      if (colModel[i].name != "rn" && colModel[i].name != "cb" && "counter" in colModel[i] && !('alwayshidden' in colModel[i]))
      {
        colArray.push([colModel[i].name, colModel[i].hidden, colModel[i].width]);
        if (colModel[i].frozen) maxfrozen = parseInt(i) + 1 - skipped;
      }
      else if (colModel[i].name == 'columns' || colModel[i].name == 'graph')
        pivot = true;
      else
        skipped++;
    }
  	var result = {"rows": colArray};
    var filter = $('#grid').getGridParam("postData").filters;
    if (typeof filter !== 'undefined' && filter.rules != [])
    	result["filter"] = filter;
    var sidx = $('#grid').getGridParam('sortname');    
    if (sidx !== '') {
      // Report is sorted
    	result['sidx'] = sidx;
    	result['sord'] = $('#grid').getGridParam('sortorder');
    }
    if (pivot) {
    	result['crosses'] = [];
      for (var i in cross_idx)
      	result['crosses'].push(cross[cross_idx[i]].key);
    }
    else
    	result['frozen'] = maxfrozen;
    return result;
  },
  
  // Save the customized column configuration
  saveColumnConfiguration : function(pgButton, indx)
  {
    // This function can be called with different arguments:
    //   - no arguments, when called from our code
    //   - paging button string, when called from jqgrid paging event
    //   - number argument, when called from jqgrid resizeStop event
    //   - function argument, when you want to run a callback function after the save
    var colArray = new Array();
    var colModel = $("#grid").jqGrid('getGridParam', 'colModel');
    var maxfrozen = 0;
    var pivot = false;
    var skipped = 0;
    var page = $('#grid').jqGrid('getGridParam', 'page');
    if (typeof pgButton === 'string')
    {
      // JQgrid paging gives only the current page
      if (pgButton.indexOf("next") >= 0)
        ++page;
      else if (pgButton.indexOf("prev") >= 0)
        --page;
      else if (pgButton.indexOf("last") >= 0)
        page = $("#grid").jqGrid('getGridParam', 'lastpage');
      else if (pgButton.indexOf("first") >= 0)
        page = 1;
      else if (pgButton.indexOf("user") >= 0)
        page = $('input.ui-pg-input').val();
    }
    else if (typeof indx != 'undefined' && colModel[indx].name == "operationplans")
      // We're resizing a Gantt chart column. Not too clean to trigger the redraw here, but so be it...
      gantt.redraw();
    for (var i in colModel)
    {
      if (colModel[i].name != "rn" && colModel[i].name != "cb" && "counter" in colModel[i] && !('alwayshidden' in colModel[i]))
      {
        colArray.push([colModel[i].name, colModel[i].hidden, colModel[i].width]);
        if (colModel[i].frozen) maxfrozen = parseInt(i) + 1 - skipped;
      }
      else if (colModel[i].name == 'columns' || colModel[i].name == 'graph')
        pivot = true;
      else
        skipped++;
    }
    var result = {
    	 [reportkey]: {
    	   "rows": colArray,
         "page": page,
         "favorites": favorites
       }};
    var tmp = $('#grid').getGridParam("postData");
    var filter = tmp ? tmp.filters : initialfilter;
    if (typeof filter !== 'undefined' && filter.rules != [])
      result[reportkey]["filter"] = filter;
    var sidx = $('#grid').getGridParam('sortname');    
    if (sidx !== '') {
      // Report is sorted
      result[reportkey]['sidx'] = sidx;
      result[reportkey]['sord'] = $('#grid').getGridParam('sortorder');
    }
    if (pivot) {
      result[reportkey]['crosses'] = [];
      for (var i in cross_idx)
      	result[reportkey]['crosses'].push(cross[cross_idx[i]].key);
    }
    else
      result[reportkey]['frozen'] = maxfrozen;
    if (typeof extraPreference == 'function')
    {
      var extra = extraPreference();
      for (var idx in extra)
        result[reportkey][idx] = extra[idx];
    }
    if (typeof url_prefix != 'undefined')
      var url = url_prefix + '/settings/';
    else
      var url = '/settings/';
    $.ajax({
      url: url,
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(result),
      success: function() {
        preferences = result;
        if (typeof pgButton === 'function')
          pgButton();
      },
      error: ajaxerror
    });
  },

  //This function is called when a cell is just being selected in an editable
  //grid. It is used to either a) select the content of the cell (to make
  //editing it easier) or b) display a date picker it the field is of type
  //date.
  afterEditCell: function (rowid, cellname, value, iRow, iCol)
  {
  var colmodel = $(this).jqGrid('getGridParam', 'colModel')[iCol];
  var iconslist = {
      time: 'fa fa-clock-o',
      date: 'fa fa-calendar',
      up: 'fa fa-chevron-up',
      down: 'fa fa-chevron-down',
      previous: 'fa fa-chevron-left',
      next: 'fa fa-chevron-right',
      today: 'fa fa-bullseye',
      clear: 'fa fa-trash',
      close: 'fa fa-remove'
    };

  if (colmodel.formatter == 'date') {
    if (colmodel.formatoptions['srcformat'] == "Y-m-d")
      $("#" + iRow + '_' + cellname).on('focusin', function() {
        $(this).parent().css({'position': 'relative', 'overflow': 'visible'});
        $(this).datetimepicker({format: 'YYYY-MM-DD', useCurrent: false, calendarWeeks: true, icons: iconslist, locale: document.documentElement.lang, widgetPositioning: {horizontal: 'auto', vertical: (iRow < 11 ?'bottom':'auto')}});
      });
    else
      $("#" + iRow + '_' + cellname).on('focusin', function() {
        $(this).parent().css({'position': 'relative', 'overflow': 'visible'});
        $(this).datetimepicker({format: 'YYYY-MM-DD HH:mm:ss', useCurrent: false, calendarWeeks: true, icons: iconslist, locale: document.documentElement.lang, widgetPositioning: {horizontal: 'auto', vertical: (iRow < 11 ?'bottom':'auto')}});
      });
  }
  else
	  $("#" + iRow + '_' + cellname).select();
  },

  showExport: function(only_list, scenario_permissions)
  {
    $('#timebuckets').modal('hide');
    $.jgrid.hideModal("#searchmodfbox_grid");

    // Prepare upfront the html for the scenarios to export
    // We limit the list of scenarios to 6
    if (scenario_permissions.length > 0) {
    	var cb = "";
    	for (var i = 0 ; i < scenario_permissions.length; i++) {
    		if (scenario_permissions[i][2] == 1)
    		cb += 
    			'<div class="form-check" style="white-space: nowrap">' +
    			'<input class="form-check-input" type="checkbox" value="" id="'+ scenario_permissions[i][0] +'" checked disabled>' +
    			'&nbsp;&nbsp;&nbsp;<label class="form-check-label" for="'+ scenario_permissions[i][0] +'">' +
    			gettext(scenario_permissions[i][1]) +
    		    '</label>' +
    		    '</div>';
    	}
    	for (var i = 0 ; i < scenario_permissions.length && i < 6; i++) {
    		if (scenario_permissions[i][2] != 1)
    		cb += 
    			'<div class="form-check" style="white-space: nowrap">' +
    			'<input class="form-check-input" type="checkbox" value="" id="'+ scenario_permissions[i][0] +'">' +
    			'&nbsp;&nbsp;&nbsp;<label class="form-check-label" for="'+ scenario_permissions[i][0] +'">' +
    			gettext(scenario_permissions[i][1]) +
    		    '</label>' +
    		    '</div>';
    	}
    }
    
    // The only_list argument is true when we show a "list" report.
    // It is false for "table" reports.
    if (only_list && scenario_permissions.length > 1)
      $('#popup').html('<div class="modal-dialog" style="width: 400px;">'+
          '<div class="modal-content">'+
            '<div class="modal-header">'+
            '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>'+
              '<h4 class="modal-title text-capitalize-first">'+gettext("Export CSV or Excel file")+'</h4>'+
            '</div>'+
            '<div class="modal-body">'+
            '<table class="table table-borderless">' +
            '<thead>' +
              '<tr>' +
                '<th scope="col">' + gettext("Export format") + '</th>' +
                '<th scope="col">' + gettext("Scenarios to export") + '</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              '<tr>' +
                '<td style="white-space: nowrap">' + 
                '<div class="radio" name="csvformat" id="csvformat" value="spreadsheetlist">' +
                '<label><input type="radio" name="csvformat" value="spreadsheetlist" checked="">' + gettext("Spreadsheet list") + '</label><br>' +
                '<label><input type="radio" name="csvformat" value="csvlist">' + gettext("CSV list") + '</label><br>' +
                '</div>' +
                '<label><b>' + gettext("Data source URL") + '</b></label>&nbsp;&nbsp;' + 
                '<a href="' + documentation + 'user-interface/getting-around/exporting-data.html" target="_blank" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                gettext("Using this link external applications can pull data from frePPLe") + '">' +
                '<span class="fa fa-question-circle"></span>' +
                '</a><br>' +         
                '<div class="input-group">' +                 
                '<input type="text" readonly id="urladdress" class="form-control" style="background: white"/>' +
                '<span class="input-group-btn">' +
                '<button type="button" class="btn btn-default fa fa-clipboard" id="copybutton" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                gettext("Copy to clipboard") + '"/></span>' +
                '</div>' +
                '</td>' +
                '<td>' +
                '<div class="check" name="scenarios" id="scenarios" value="default">' +
                cb +                 
               '</div>' +
                '</td>' +
              '</tr>' +
            '</tbody>' +
          '</table>' +
            '</div>'+
            '<div class="modal-footer">'+
              '<input type="submit" id="exportbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Export')+'">'+
              '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
            '</div>'+
          '</div>'+
      '</div>' )
      .modal('show');
    else if (!only_list && scenario_permissions.length > 1)
        $('#popup').html('<div class="modal-dialog" style="width: 400px;">'+
                '<div class="modal-content">'+
                  '<div class="modal-header">'+
                  '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>'+
                    '<h4 class="modal-title text-capitalize-first">'+gettext("Export CSV or Excel file")+'</h4>'+
                  '</div>'+
                  '<div class="modal-body">'+
                  '<table class="table table-borderless">' +
                  '<thead>' +
                    '<tr>' +
                      '<th scope="col">' + gettext("Export format") + '</th>' +
                      '<th scope="col">' + gettext("Scenarios to export") + '</th>' +
                    '</tr>' +
                  '</thead>' +
                  '<tbody>' +
                    '<tr>' +
                      '<td>' + 
                      '<div class="radio" name="csvformat" id="csvformat" value="spreadsheetlist">' +
                      '<label><input type="radio" name="csvformat" value="spreadsheettable" checked="">' + gettext("Spreadsheet table") + '</label><br>' +
                      '<label><input type="radio" name="csvformat" value="spreadsheetlist">' + gettext("Spreadsheet list") + '</label><br>' +
                      '<label><input type="radio" name="csvformat" value="csvtable">' + gettext("CSV table") + '</label><br>' +
                      '<label><input type="radio" name="csvformat" value="csvlist">' + gettext("CSV list") + '</label><br>' +
                      '</div>' +
                      '<label><b>' + gettext("Data source URL") + '</b></label>&nbsp;&nbsp;' + 
                      '<a href="' + documentation + 'user-interface/getting-around/exporting-data.html" target="_blank" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                      gettext("Using this link external applications can pull data from frePPLe") + '">' +
                      '<span class="fa fa-question-circle"></span>' +
                      '</a><br>' +         
                      '<div class="input-group">' +                 
                      '<input type="text" readonly id="urladdress" class="form-control" style="background: white"/>' +
                      '<span class="input-group-btn">' +
                      '<button type="button" class="btn btn-default fa fa-clipboard" id="copybutton" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                      gettext("Copy to clipboard") + '"/></span>' +
                      '</div>' +
                      '</td>' +
                      '<td>' +
                      '<div class="check" name="scenarios" id="scenarios" value="default">' +
                      cb +                 
                     '</div>' +
                      '</td>' +
                    '</tr>' +
                  '</tbody>' +
                '</table>' +
                  '</div>'+
                  '<div class="modal-footer">'+
                    '<input type="submit" id="exportbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Export')+'">'+
                    '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
                  '</div>'+
                '</div>'+
            '</div>' )
            .modal('show');
    else if (only_list && scenario_permissions.length <= 1)
        $('#popup').html('<div class="modal-dialog" style="width: 400px;">'+
                '<div class="modal-content">'+
                  '<div class="modal-header">'+
                  '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>'+
                    '<h4 class="modal-title text-capitalize-first">'+gettext("Export CSV or Excel file")+'</h4>'+
                  '</div>'+
                  '<div class="modal-body">'+
                    '<label class="control-label"><b>' + gettext("Export format") +
                      '</b><div class="radio" name="csvformat" id="csvformat" value="spreadsheetlist">' +
                        '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="spreadsheetlist" checked="">' + gettext("Spreadsheet list") + '</label><br>' +
                        '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="csvlist">' + gettext("CSV list") + '</label><br>' +
                      '</div>' +
                    '</label><br>' +
                    '<label><b>' + gettext("Data source URL") + '</b></label>&nbsp;&nbsp;' + 
                    '<a href="' + documentation + 'user-interface/getting-around/exporting-data.html" target="_blank" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                    gettext("Using this link external applications can pull data from frePPLe") + '">' +
                    '<span class="fa fa-question-circle"></span>' +
                    '</a><br>' +         
                    '<div class="input-group">' +                 
                    '<input type="text" readonly id="urladdress" class="form-control" style="background: white"/>' +
                    '<span class="input-group-btn">' +
                    '<button type="button" class="btn btn-default fa fa-clipboard" id="copybutton" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                    gettext("Copy to clipboard") + '"/></span>' +
                    '</div>' +
                    '</label><br>' +
                  '<div class="modal-footer">'+
                    '<input type="submit" id="exportbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Export')+'">'+
                    '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
                  '</div>'+
                '</div>'+
            '</div>' )
            .modal('show');
    else if (!only_list && scenario_permissions.length <= 1)
    	$('#popup').html('<div class="modal-dialog" style="width: 400px;">'+
    	          '<div class="modal-content">'+
    	            '<div class="modal-header">'+
    	              '<h4 class="modal-title">'+gettext("Export CSV or Excel file")+'</h4>'+
    	            '</div>'+
    	            '<div class="modal-body">'+
    	              '<label class="control-label"><b>' + gettext("Export format") +
    	                '</b><div class="radio" name="csvformat" id="csvformat" value="spreadsheettable">' +
    	                  '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="spreadsheettable" checked="">' + gettext("Spreadsheet table") + '</label><br>' +
    	                  '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="spreadsheetlist">' + gettext("Spreadsheet list") + '</label><br>' +
    	                  '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="csvtable">' + gettext("CSV table") + '</label><br>' +
    	                  '&nbsp;&nbsp;&nbsp;&nbsp;<label><input type="radio" name="csvformat" value="csvlist">' + gettext("CSV list") + '</label><br>' +
    	                '</div>' +
    	              '</label>' + '<br>' +
                    '<label><b>' + gettext("Data source URL") + '</b></label>&nbsp;&nbsp;' + 
                    '<a href="' + documentation + 'user-interface/getting-around/exporting-data.html" target="_blank" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                    gettext("Using this link external applications can pull data from frePPLe") + '">' +
                    '<span class="fa fa-question-circle"></span>' +
                    '</a><br>' +         
                    '<div class="input-group">' +                 
                    '<input type="text" readonly id="urladdress" class="form-control" style="background: white"/>' +
                    '<span class="input-group-btn">' +
                    '<button type="button" class="btn btn-default fa fa-clipboard" id="copybutton" data-toggle="tooltip" data-placement="top" data-original-title="' + 
                    gettext("Copy to clipboard") + '"/></span>' +
    	            '</div>'+
    	            '<div class="modal-footer">'+
    	              '<input type="submit" id="exportbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Export')+'">'+
    	              '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
    	            '</div>'+
    	          '</div>'+
    	      '</div>' )
    	      .modal('show');
    
    // initialize the data source url
    update_datasource_url();
 
 	// Update url when the scenario selection changes
    for (var i = 0 ; i < scenario_permissions.length && i < 6; i++) {
		if (scenario_permissions[i][2] != 1)
		  $('#' + scenario_permissions[i][0]).on('click', function() {
			  update_datasource_url();
		  });
	}
    
    $('[data-toggle="tooltip"]').tooltip({delay: { "show": 500, "hide": 100 }});
    
    $('#copybutton').on('click', function() {
    	// should be up to date but let's recompute it.
    	update_datasource_url();
    	$('#urladdress').select();
    	document.execCommand('copy');
    	
    });
    
       //Compute the power query url to display
     function update_datasource_url() {
	     
	     var url = (location.href.indexOf("#") != -1 ? 
	     		location.href.substr(0,location.href.indexOf("#")) : location.href);
	     
	 	
	 	if (location.search.length > 0)
	 	      // URL already has arguments
	 	    	url += "&";
		    else if (url.charAt(url.length - 1) != '?')
		      // This is the first argument for the URL
		    	url += "?";

	 	// csvtable and spreadsheet table are converted into csvlist
	 	// Maintaining a table view with buckets as columns won't work with Excel after a bucket shift
	 	url += "format=" + 
	 	(only_list ? "csv": "csvlist");
	 	
	 	// retrieve all columns from the view
	 	url +=  "&allcolumns=true";
	 	
	 	if (scenario_permissions.length > 1) {
		      var firstTime = true;
		      var scenarios = "";
		      for (var i = 0 ; i < scenario_permissions.length; i++) {
		    	  if ($('#' + scenario_permissions[i][0]).is(":checked")) {
		    	  	if (firstTime)
		    	  		firstTime = false;
		    	  	else
		    	  		scenarios += ",";
		    	  			
		    	    scenarios += scenario_permissions[i][0];
		    	  }
		      }
		      url += "&scenarios=" + scenarios;
	     }   	
	 	$('#urladdress').val(url);
	 }
    
    $('#exportbutton').on('click', function() {
      // Fetch the report data
      var url = (location.href.indexOf("#") != -1 ? location.href.substr(0,location.href.indexOf("#")) : location.href);
      var scenarios = "";
      if (scenario_permissions.length > 1) {
	      var firstTime = true;
	      for (var i = 0 ; i < scenario_permissions.length; i++) {
	    	  if ($('#' + scenario_permissions[i][0]).is(":checked")) {
	    	  	if (firstTime)
	    	  		firstTime = false;
	    	  	else
	    	  		scenarios += ",";
	    	  			
	    	    scenarios += scenario_permissions[i][0];
	    	  }
	      }
      }
      
      if (location.search.length > 0)
        // URL already has arguments
        url += "&format=" + $('#csvformat input:radio:checked').val();
      else if (url.charAt(url.length - 1) == '?')
        // This is the first argument for the URL, but we already have a question mark at the end
        url += "format=" + $('#csvformat input:radio:checked').val();
      else
        // This is the first argument for the URL
        url += "?format=" + $('#csvformat input:radio:checked').val();
      
      // Append scenarios if needed
      if (scenario_permissions.length > 1)
    	  url += "&scenarios=" + scenarios;
      
      // Append current filter and sort settings to the URL
      var postdata = $("#grid").jqGrid('getGridParam', 'postData');
      url +=  "&" + jQuery.param(postdata);
      // Open the window
      window.open(url,'_blank');
      $('#popup').modal('hide');
    });
  },


  // Display time bucket selection dialog
  showBucket: function()
  {
    // Show popup
    $('#popup').modal('hide');
    $.jgrid.hideModal("#searchmodfbox_grid");
    var iconslist = {
      time: 'fa fa-clock-o',
      date: 'fa fa-calendar',
      up: 'fa fa-chevron-up',
      down: 'fa fa-chevron-down',
      previous: 'fa fa-chevron-left',
      next: 'fa fa-chevron-right',
      today: 'fa fa-bullseye',
      clear: 'fa fa-trash',
      close: 'fa fa-remove'
    };
    $("#horizonstart").parent().datetimepicker({
    	  format: 'YYYY-MM-DD',
    	  calendarWeeks: true,
    	  icons: iconslist,
    	  locale: document.documentElement.lang
    	  });
    $("#horizonend").parent().datetimepicker({
    	  format: 'YYYY-MM-DD',
    	  calendarWeeks: true,
    	  icons: iconslist,
    	  locale: document.documentElement.lang
    	  });
    $("#horizonstart").parent().on("dp.change", function (selected) {
      $("#horizonend").parent().data("DateTimePicker").minDate(selected.date);
      });
    $( "#okbutton" ).on('click', function() {
            // Compare old and new parameters
            var params = $('#horizonbuckets').val() + '|' +
              $('#horizonstart').val() + '|' +
              $('#horizonend').val() + '|' +
              ($('#horizontype').is(':checked') ? "True" : "False") + '|' +
              $('#horizonbefore').val() + '|' +
              $('#horizonlength').val() + '|' +
              $('#horizonunit').val();

            if (params == $('#horizonoriginal').val())
              // No changes to the settings. Close the popup.
              $("#timebuckets").modal('hide');
            else {
              // Ajax request to update the horizon preferences
              $.ajax({
                  type: 'POST',
                  url: url_prefix + '/horizon/',
                  data: {
                    horizonbuckets: $('#horizonbuckets').val() ?
                      $('#horizonbuckets').val() :
                      $("#horizonbucketsul li a").first().text(),
                    horizonstart: $('#horizonstart').val(),
                    horizonend: $('#horizonend').val(),
                    horizontype: ($('#horizontype').is(':checked') ? '1' : '0'),
                    horizonlength: $('#horizonlength').val(),
                    horizonbefore: $('#horizonbefore').val(),
                    horizonunit: $('#horizonunit').val()
                    },
                  dataType: 'text/html',
                  async: false  // Need to wait for the update to be processed!
                });
            // Reload the report
            window.location.href = window.location.href;
            }});
    $('#timebuckets').modal('show');
         },

  //Display dialog for copying or deleting records
  showDelete : function(url)
  {
    if ($('#delete_selected').hasClass("disabled")) return;
    var sel = jQuery("#grid").jqGrid('getGridParam','selarrrow');
    if (sel.length == 1)
      // Redirect to a page for deleting a single entity
      location.href = url + admin_escape(sel[0]) + '/delete/';
    else if (sel.length > 0)
    {
     $('#timebuckets').modal('hide');
     $.jgrid.hideModal("#searchmodfbox_grid");
     $('#popup').html('<div class="modal-dialog">'+
             '<div class="modal-content">'+
               '<div class="modal-header">'+
                 '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
                 '<h4 class="modal-title text-capitalize-first">'+gettext('Delete data')+'</h4>'+
               '</div>'+
               '<div class="modal-body">'+
                 '<p>'+interpolate(gettext('You are about to delete %s objects AND ALL RELATED RECORDS!'), [sel.length], false)+'</p>'+
               '</div>'+
               '<div class="modal-footer">'+
                 '<input type="submit" id="delbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Confirm')+'">'+
                 '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
               '</div>'+
             '</div>'+
         '</div>' )
         .modal('show');
     $('#delbutton').on('click', function() {
               $.ajax({
                 url: url,
                 data: JSON.stringify([{'delete': sel}]),
                 type: "POST",
                 contentType: "application/json",
                 success: function () {
               $("#delete_selected").prop("disabled", true).removeClass("bold");
               $("#copy_selected").prop("disabled", true).removeClass("bold");
                   $('.cbox').prop("checked", false);
                   $('#cb_grid.cbox').prop("checked", false);
                   $("#grid").trigger("reloadGrid");
               $('#popup').modal('hide');
                   },
                 error: function (result, stat, errorThrown) {
               $('#popup .modal-body p').html(result.responseText);
               $('#popup .modal-title').html(gettext("Error"));
               $('#popup .modal-header').addClass('bg-danger');
               $('#delbutton').prop("disabled", true).hide();
                   }
           })
         })
             }
           },

  showCopy: function()
  {
   if ($('#copy_selected').hasClass("disabled")) return;
   var sel = jQuery("#grid").jqGrid('getGridParam','selarrrow');
   if (sel.length > 0)
   {
     $('#timebuckets').modal('hide');
     $.jgrid.hideModal("#searchmodfbox_grid");
     $('#popup').html('<div class="modal-dialog">'+
             '<div class="modal-content">'+
               '<div class="modal-header">'+
                 '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
                 '<h4 class="modal-title text-capitalize-first">'+gettext("Copy data")+'</h4>'+
                 '</div>'+
                 '<div class="modal-body">'+
                   '<p>'+interpolate(gettext('You are about to duplicate %s objects'), [sel.length], false)+'</p>'+
                   '</div>'+
                   '<div class="modal-footer">'+
                     '<input type="submit" id="copybutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Confirm')+'">'+
                     '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
                   '</div>'+
                 '</div>'+
             '</div>' )
     .modal('show');
     $('#copybutton').on('click', function() {
               $.ajax({
                 url: location.pathname,
                 data: JSON.stringify([{'copy': sel}]),
                 type: "POST",
                 contentType: "application/json",
                 success: function () {
           $("#delete_selected").prop("disabled", true).removeClass("bold");
           $("#copy_selected").prop("disabled", true).removeClass("bold");
                   $('.cbox').prop("checked", false);
                   $('#cb_grid.cbox').prop("checked", false);
                   $("#grid").trigger("reloadGrid");
           $('#popup').modal('hide');
                   },
                 error: function (result, stat, errorThrown) {
           $('#popup .modal-body p').html(result.responseText);
           $('#popup .modal-title').html(gettext("Error"));
           $('#popup .modal-header').addClass('bg-danger');
           $('#copybutton').prop("disabled", true).hide();
                   }
       })
     })
   }
  },

  // Display filter dialog
  showFilter: function(gridid, curfilterid, filterid)
  {
	  $("#addsearch").val("");
	  $("#filterfield").remove();
	  grid.handlerinstalled = false;
    $('#popup').modal("hide");
    $('#timebuckets').modal('hide');
  	var thegridid = (typeof gridid !== 'undefined') ? gridid : "grid";
  	var thegrid = $("#" + thegridid);
  	var curfilter = $((typeof curfilterid !== 'undefined') ? curfilterid : "#curfilter");
    $('.modal').modal('hide');
    thegrid.jqGrid('searchGrid', {
      closeOnEscape: true,
      multipleSearch:true,
      multipleGroup:true,
      overlay: 0,
      sopt: ['eq','ne','lt','le','gt','ge','bw','bn','in','ni','ew','en','cn','nc'],
      onSearch : function() {
        var c = $("#fbox_" + thegridid).jqFilter('filterData');
        grid.saveColumnConfiguration();
        grid.getFilterGroup(thegrid, c, true, curfilter);
        if (typeof extraSearchUpdate == 'function')
          extraSearchUpdate(c);
        },
      onReset : function() {        
        if (typeof initialfilter !== 'undefined') {
        	thegrid.jqGrid('getGridParam','postData').filters = JSON.stringify(initialfilter);
        	grid.getFilterGroup(thegrid, initialfilter, true, curfilter);
        }
        else
        	curfilter.html("");
        grid.saveColumnConfiguration();
        return true;
        }
      });
    $("#searchmodfbox_grid").detach().appendTo("#content-main");
  },
  
  countFilters: 0,
  
  handlerinstalled: false,
  
  addFilter: function(event) {
    if (event) {
    	event.stopPropagation();
  	  event.preventDefault();
  	  var field = $(event.target).attr("data-filterfield");
    }
    else 
      var field = $("#filterfield [data-filterfield]").first().attr("data-filterfield");
  	var n = {
				"field": field,
				"op":"cn",
				"data": $("#addsearch").val(),
				"filtercount":++grid.filtercount
				};
    var c = $('#grid').getGridParam("postData");
    c = (c !== undefined) ? c.filters : initialfilter;
    if (c && c !== "") {
      c = JSON.parse(c);
      if (c["groupOp"] == "AND")
        // Add condition to existing and-filter
        c["rules"].push(n);
      else
        // Wrap existing filter in a new and-filter
        c = {
          "groupOp":"AND",
          "rules":[n],
          "groups":[c]
          };
		}
		else {
      // First filter
      c = {
        "groupOp":"AND",
        "rules":[n],
        "groups":[]
        };
		}
		$("#grid").setGridParam({
      postData:{filters: JSON.stringify(c)},
      search:true
      }).trigger('reloadGrid');
		grid.saveColumnConfiguration();
  	if (typeof extraSearchUpdate == 'function')
  		extraSearchUpdate(c);
		grid.getFilterGroup($("#grid"), c, true,  $("#curfilter"));
		$(document).off("click", grid.clickFilter);
		grid.handlerinstalled = false;
	  $("#addsearch").val("");
	  $("#filterfield").remove();
	  $("#tooltip").css("display", "none");
  },
  
  clickFilter: function(event) {
  	if ($(event.target).attr('id') != "addsearch") {
  		$(document).off("click", grid.clickFilter);
  		grid.handlerinstalled = false;
  	  $("#addsearch").val("");
  	  $("#filterfield").remove();
  	}
  },
    
  showFilterList: function(el) {
  	$.jgrid.hideModal("#searchmodfbox_grid");
  	event.stopPropagation();
    if (!grid.handlerinstalled) {
      $(document).on("click", grid.clickFilter);
    	var l = $('<span id="filterfield" class="list-group">');
      var cnt = 15;  // Limits the number fields to choose from
      for (var col of $("#grid").jqGrid('getGridParam', 'colModel')) {
      	var searchoptions =  col.searchoptions;
      	if (searchoptions && searchoptions.sopt && searchoptions.sopt.includes("cn")) {
      		var n = $('<button type="button" class="list-group-item list-group-item-action" onclick="grid.addFilter(event)" />');
      		n.attr("data-filterfield", col.name);
      		n.html(gettext("Search") + ' ' + col.label);
      		l.append(n);
      		if (--cnt <= 0) break;
      	}
      }
    	$(el).parent().before(l);
      grid.handlerinstalled = true;
    }    
  },
  
  keyDownSearch: function() {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == 13)
      grid.addFilter();
  },
  
  updateFilter: function(obj, idx, newvalue) {
    if (obj instanceof Array)
    	for (var i in obj)
    		grid.updateFilter(obj[i], idx, newvalue);
    else if (typeof obj == "object") {
    	for (var i in obj) {
    		if (i == "filtercount" && obj[i] == idx)
      		obj.data = newvalue;
    		else if (obj.hasOwnProperty(i))
    			grid.updateFilter(obj[i], idx, newvalue);
    	}
    }
  },
  
  removeFilter: function(obj, idx) {
    if (obj instanceof Array)
    	for (var i in obj) {
    		if (obj[i]["filtercount"] == idx)
    			obj.splice(i, 1);
    		else if (obj[i]["filtercount"] > idx)
    			--obj[i]["filtercount"];
    		else
    			grid.removeFilter(obj[i], idx);
    	}
    else if (typeof obj == "object") {    	
    	for (var i in obj) {    		
    		if (obj.hasOwnProperty(i))
    			grid.removeFilter(obj[i], idx);
    	}
    }
  },
  
  getFilterRule: function(thegrid, rule, thefilter, fullfilter)
  {
    // Find the column
    var i, col, oper;
    var columns = thegrid.jqGrid ('getGridParam', 'colModel');
    for (i = 0; i < columns.length; i++) {
      if(columns[i].name === rule.field || columns[i].field_name === rule.field) {
        col = columns[i];
        break;
      }
    }
    if (col == undefined)
    	return;
    
    // Find operator
    if (rule.op == "win")
      oper = gettext("within");
    else if (rule.op == "ico")
        oper = gettext("is child of"); 
    else {
      for (var firstKey in $.jgrid.locales)
        var operands = $.jgrid.locales[firstKey].search.odata;
      for (i = 0; i < operands.length; i++)
        if (operands[i].oper == rule.op) {
          oper = operands[i].text;
          break;
        }
      if (oper == undefined)
    	  oper = rule.op;
    }

    // Final result  	
  	var newexpression = $('<span class="label label-default">' + col.label + '&nbsp;' + oper + '&nbsp;</span>');
    var newelement = $('<input size="10">');
    rule["filtercount"] = grid.countFilters++;  // Mark position in the expression
    newelement.val(rule.data);
    newelement.on('change', function(event) {
      grid.updateFilter(fullfilter, rule["filtercount"], $(event.target).val());
    	thegrid.setGridParam({
        postData:{filters: JSON.stringify(fullfilter)},
        search:true
        }).trigger('reloadGrid');
    	if (typeof extraSearchUpdate == 'function')
    		extraSearchUpdate(fullfilter);
    	grid.saveColumnConfiguration();
    	});
    newexpression.append(newelement);
    newexpression.append('&nbsp;');    
    if (rule.op == "win")
      // Special case for the "within N days" operator
    	newexpression.append(gettext("days") + '&nbsp;');
    var deleteelement = $('<span class="fa fa-times"/>');
    deleteelement.on('click', function(event) {
    	grid.removeFilter(fullfilter, rule["filtercount"]);
    	grid.getFilterGroup(thegrid, fullfilter, true, thefilter, fullfilter);
    	thegrid.setGridParam({
        postData:{filters: JSON.stringify(fullfilter)},
        search:true
        }).trigger('reloadGrid');
    	if (typeof extraSearchUpdate == 'function')
    		extraSearchUpdate(fullfilter);
    	grid.saveColumnConfiguration(); 
    });
    newexpression.append(deleteelement);
    thefilter.append(newexpression);
  },
  
  getFilterGroup: function(thegrid, group, first, thefilter, fullfilter)
  {
    if (!first)
    	thefilter.append("( ");
    else {
    	thefilter.html("");
    	fullfilter = group;
    	grid.countFilters = 0;
    }
    
    if (group !== null && group !== undefined && group.groups !== undefined) {    	
      for (var index = 0; index < group.groups.length; index++) {
        if (thefilter.html().length > 2) {
          if (group.groupOp === "OR")
          	thefilter.append(" " + gettext("or") + " ");
          else
            thefilter.append(" " + gettext("and") + " ");
        }
        grid.getFilterGroup(thegrid, group.groups[index], false, thefilter, fullfilter);
      }
    }

    if (group !== null && group !== undefined && group.rules !== undefined) {
      for (var index = 0; index < group.rules.length; index++) {
        if (thefilter.html().length > 2)
          thefilter.append( " " + gettext((group.groupOp === "OR") ? "or" : "and") + " ");
        grid.getFilterRule(thegrid, group.rules[index], thefilter, fullfilter);
      }
    }

    if (!first) thefilter.append("&nbsp;)");
  },
  
  markSelectedRow: function(sel)
  {
    if (typeof sel==='undefined') {
      sel = 0;
    }

    if (sel > 0)
    {
      $("#copy_selected").prop('disabled', false).addClass("bold");
      $("#delete_selected").prop('disabled', false).addClass("bold");
      if ($("#actions").length) $("#actions1").prop('disabled', false);
    }
    else
    {
      $("#copy_selected").prop('disabled', true).removeClass("bold");
      $("#delete_selected").prop('disabled', true).removeClass("bold");
      if ($("#actions").length) $("#actions1").prop('disabled', true);
    }
  },

  markAllRows: function()
  {
    if ($(this).is(':checked'))
    {
      $("#copy_selected").prop('disabled', false).addClass("bold");
      $("#delete_selected").prop('disabled', false).addClass("bold");
      if ($("#actions").length) $("#actions1").prop('disabled', false);
      $('.cbox').prop("checked", true);
    }
    else
    {
      $("#copy_selected").prop('disabled', true).removeClass("bold");
      $("#delete_selected").prop('disabled', true).removeClass("bold");
      if ($("#actions").length) $("#actions1").prop('disabled', true);
      $('.cbox').prop("checked", false);
    }
  },

  displayMode: function(m)
  {
    var url = (location.href.indexOf("#") != -1 ? location.href.substr(0,location.href.indexOf("#")) : location.href);
    if (location.search.length > 0)
      // URL already has arguments
      url = url.replace("&mode=table","").replace("&mode=graph","").replace("mode=table","").replace("mode=graph","") + "&mode=" + m;
    else if (url.charAt(url.length - 1) == '?')
      // This is the first argument for the URL, but we already have a question mark at the end
      url += "mode=" + m;
    else
      // This is the first argument for the URL
      url += "?mode=" + m;
    window.location.href = url;
  }
}

//
// Functions to manage favorites
//

var favorite = {
		
	  check: function() {
	  	var fav = $("#favoritename").val();
	  	if (fav.length > 0 && (
	  			(typeof favorites !== 'undefined' && !(fav in favorites))
	  			|| (typeof preferences !== 'undefined' && !("favorites" in preferences))
	  			|| (typeof preferences !== 'undefined' && "favorites" in preferences && !(fav in preferences.favorites))
	  			)) {
	      $("#favoritesave").removeClass("disabled");
	  	  return true;
	  	}
	  	else {
	  	  $("#favoritesave").addClass("disabled");
	  	  return false;
	  	}
	  },
	  
	  save: function() {
	  	var fav = $("#favoritename").val();
	  	if (!favorite.check()) return;
	  	favorites[fav] = grid.getGridConfig();
	  	grid.saveColumnConfiguration();
	  	var divider = $("#favoritelist li.divider");
	    if (divider.length == 0) {
	    	$("#favoritelist").prepend('<li role="separator" class="divider"></li>');
	    	divider = $("#favoritelist li.divider");
	    }
	    var newfav_li = $('<li id="zorro"></li>');
	    var newfav_a = $('<a href="#" onclick="favorite.open(event)"></a>');
	    newfav_a.text(fav);
	    newfav_a.append(
	    		'<div style="float:right"><span class="fa fa-trash-o" onclick="favorite.remove(event)"></span></div>'
	    		);
	    newfav_li.append(newfav_a);
	    divider.before(newfav_li);
	    favorite.check();
	  },
	  
	  remove: function(event) {
	  	var fav = $(event.target).closest("a").text();
	  	if (fav in favorites) {
		  	if (confirm(gettext("Click ok to confirm deleting the favorite"))) {
	  		  delete favorites[fav];
	  	    grid.saveColumnConfiguration();
	  	    $(event.target).closest("li").remove();
	  	    $("#favoritename").val(fav);
	  	    favorite.check();
		  	}
	  	}
	  	event.stopImmediatePropagation();
	  },
	  
	  open: function(event) {
	  	var fav = $(event.target).parent().text();
	  	if (!(fav in favorites)) return;

	  	var thegrid = $("#grid");
	  	var graph = false;
	  	var pivot = false;
	  	var skipped = 0;
    	var colModel = thegrid.jqGrid('getGridParam', 'colModel');
    	var numfrozen = favorites[fav]["frozen"];
    	for (var i in colModel) {
    		if (colModel[i].name == 'graph') graph = true;
    		else if (colModel[i].name == 'columns') {
    			pivot = true;
    			numfrozen = parseInt(i);
    		}
    		else if (colModel[i].name == 'cb') skipped += 1;
      }
	  	if (!graph) thegrid.jqGrid('destroyFrozenColumns');
	  	
	  	// Restore visibility and column width	
      for (var r of favorites[fav]["rows"]) {
      	if (r[1])
      		thegrid.jqGrid("hideCol", r[0]);
      	else
      		thegrid.jqGrid("showCol", r[0]);
      	thegrid.jqGrid('setColWidth', r[0], r[2]);
      }

      // Restore crosses
      if ("crosses" in favorites[fav]) {
      	cross_idx = [];
        for (var i of favorites[fav]["crosses"]) {
        	for (var j in cross)
        		if (cross[j]["key"] == i)
        			cross_idx.push(parseInt(j));
        }
      }

    	// Reorder columns
      var perm = [];
    	for (var f of favorites[fav]["rows"]) {
    		if (!f[1]) {
    			perm.push(f[0]);    		
    		  thegrid.jqGrid('setColProp', f[0], {frozen: perm.length < numfrozen + skipped});
    		}
    	}
      if (pivot) {
      	for (var j of colModel) {
      	  if (!("counter" in j)) {
      	  	perm.push(j["name"]);
      	    j.frozen = (j.name == 'columns');
      	  }
      	  else
      	  	j.frozen = true;
      	}
      }
      for (var k of colModel) {
      	if (!perm.includes(k["name"]) && k["name"] != "cb")
      		perm.push(k["name"]);
      }
      thegrid.jqGrid("remapColumnsByName", perm, true, false);
      
      // Restore the filter
      if ("filter" in favorites[fav] && favorites[fav]["filter"] != "") {
        thegrid.setGridParam({
          postData: {filters: favorites[fav]["filter"]},
          search: true
          });
        grid.getFilterGroup($('#grid'), JSON.parse(favorites[fav]["filter"]), true, $("#curfilter"));
      }
      else {
      	thegrid.setGridParam({
          postData: {filters: ""},
          search: true
          });
        $("#curfilter").html("");
      }
      
      // Restore the sort for the backend
      var sortstring;      
	  	if ("sord" in favorites[fav] && "sidx" in favorites[fav]) {
  		  thegrid.setGridParam({
          sortname: favorites[fav]["sidx"],
          sortorder: favorites[fav]["sord"]
          });
  		  sortstring = (favorites[fav]["sidx"] + " " + favorites[fav]["sord"]).split(",");
	  	}
  		else {
  		  thegrid.setGridParam({
  		    sortname: "",
          sortorder: "asc"
          });
  		  sortstring = default_sort.split(",");
  		}
	  	
	  	// Reset the sort icons
	  	var p = thegrid.jqGrid('getGridParam');
	  	for (var k of p.colModel) {
	  		var headercell = $("#" + p.id + "_" + k["name"]);
	  		headercell.find("span.s-ico").css("display","none");
	  		headercell.find("span.ui-grid-ico-sort").addClass("disabled");
	  		headercell.find("span.ui-jqgrid-sort-order").html("&nbsp;");
	  		k.lso = "";
	  	}
	  	
	  	// Update the sort icons
	  	for (var k in sortstring) {
	  		var s = sortstring[k].trim().split(" ");
	  		var colname = s[0].trim();
	  		var headercell = $("#" + p.id + "_" + colname);
	  		headercell.find("span.s-ico").css("display","");
	  		if (s[1].trim() == "asc") {
	  		  headercell.find("span.ui-icon-asc").removeClass("disabled");
	  		  p.colModel[p.iColByName[colname]].lso = "asc-desc";
	  		}
	  		else {
	  		  headercell.find("span.ui-icon-desc").removeClass("disabled");
	  		  p.colModel[p.iColByName[colname]].lso = "desc-asc";
	  		}
  		  headercell.find("span.ui-jqgrid-sort-order").html(parseInt(k)+1);
	  	}
			
      // Refresh the data
      if (!graph) thegrid.jqGrid('setFrozenColumns');
      thegrid.trigger('reloadGrid');
      thegrid.setGridWidth($('#content-main').width());
      grid.saveColumnConfiguration();
	  }
};

//----------------------------------------------------------------------------
// Code for ERP integration
//----------------------------------------------------------------------------

var ERPconnection = {
    IncrementalExport: function(grid, transactiontype) {
      // Collect all selected rows in the status 'proposed'
      var sel = grid.jqGrid('getGridParam','selarrrow');
      if (sel === null || sel.length == 0)
        return;
      var data = [];

      for (var i in sel) {
        var r = grid.jqGrid('getRowData', sel[i]);
        if (r.type === undefined)
          r.type = transactiontype;
        if (r.status == 'proposed')
          data.push(r);
      }
      if (data == [])
        return;

      // Send to the server for upload into openbravo
      $('#timebuckets').modal('hide');
      $.jgrid.hideModal("#searchmodfbox_grid");
      $('#popup').html(''+
          '<div class="modal-dialog">'+
          '<div class="modal-content">'+
          '<div class="modal-header">'+
          '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
          '<h4 class="modal-title text-capitalize-first">'+gettext("export")+'</h4>'+
          '</div>'+
          '<div class="modal-body">'+
          '<p class="text-capitalize-first">' + gettext("export selected records") + '</p>'+
          '</div>'+
          '<div class="modal-footer">'+
          '<input type="submit" id="button_export" role="button" class="btn btn-primary pull-right" value="'+gettext('Confirm')+'">'+
          '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
          '</div>'+
          '</div>'+
      '</div>' ).modal('show');

      $('#button_export').on('click', function() {
        $('#popup .modal-body p').html(gettext('connecting') + '...');
        $.ajax({
          url: url_prefix + "/erp/upload/",
          data: JSON.stringify(data),
          type: "POST",
          contentType: "application/json",
          success: function () {
            var rowdata = [];
            // Mark selected rows as "approved" if the original status was "proposed".
            $('#popup .modal-body p').html(gettext("Export successful"));
            $('#cancelbutton').val(gettext('Close'));
            $('#button_export').removeClass("btn-primary").prop('disabled', true);

            //update both cell value and grid data
            for (var i in sel) {
              var cur = grid.jqGrid('getCell', sel[i], 'status');

              if (cur === 'proposed') {
                grid.jqGrid('setCell', sel[i], 'status', 'approved');
                rowdata = grid.jqGrid('getRowData', sel[i]);
                rowdata.status = 'approved';
              }
            };
            grid.jqGrid('setRowData', rowdata);

            if (typeof checkrows === 'function') {
              checkrows(grid, sel);
            }

          },
          error: function (result, stat, errorThrown) {
            $('#popup .modal-title').html(gettext("Error"));
            $('#popup .modal-header').addClass('bg-danger');
            $('#popup .modal-body p').html(result.responseText);
            $('#button_export').text(gettext('retry'));
          }
        });
      });
      if ($("#actions").length)
        $("#actions1 span").text($("#actionsul").children().first().text());
    },


//  ----------------------------------------------------------------------------
//  Sales Orders dependencies export
//  ----------------------------------------------------------------------------


    SODepExport: function(grid, transactiontype) {
      // Collect all selected rows in the status 'proposed'
      var sel = grid.jqGrid('getGridParam','selarrrow');
      if (sel === null || sel.length == 0)
        return;
      var data = [];

      for (var i in sel) {
        var r = grid.jqGrid('getRowData', sel[i]);
        if (r.type === undefined)
          r.type = transactiontype;
        data.push(r);
      }
      if (data == [])
        return;

      $('#timebuckets').modal('hide');
      $.jgrid.hideModal("#searchmodfbox_grid");
      $('#popup').html(''+
          '<div class="modal-dialog" style="max-height: 80%; width: 90%; visibility: hidden">'+
          '<div class="modal-content">'+
          '<div class="modal-header">'+
          '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
          '<h4 class="modal-title text-capitalize-first">'+gettext("export")+'</h4>'+
          '</div>'+
          '<div class="modal-body">'+

          '</div>'+
          '<div class="modal-footer">'+
          '<input type="submit" id="button_export" role="button" class="btn btn-primary pull-right" disabled value="'+gettext('Confirm')+'">'+
          '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Cancel')+'">'+
          '</div>'+
          '</div>'+
      '</div>' );

      // compose url
      var components='?demand=';
      for (i=0; i<sel.length; i++) {
        var r = grid.jqGrid('getRowData', sel[i]);
        if (r.type === undefined)
          r.type = transactiontype;
        if (r.status == 'open' || r.status == 'proposed') {
          if (i==0) components+=encodeURIComponent(sel[i]);
          else components+='&demand='+encodeURIComponent(sel[i]);
        };
      };

      //get demandplans
      $.ajax({
        url: url_prefix + "/demand/operationplans/" + components,
        type: "GET",
        contentType: "application/json",
        success: function (data) {
          $('#popup .modal-body').html('<div class="table-responsive">'+
              '<table class="table-condensed table-hover" id="forecastexporttable">'+
              '<thead class="thead-default">'+
              '</thead>'+
              '</table>'+
          '</div>');

          var labels = ["id","type","item","value","quantity","location","origin","startdate","enddate","criticality"];

          if (transactiontype == 'SO') {
            var tableheadercontent = $('<tr/>');

            tableheadercontent.append($('<th/>').html(
            		'<input id="cb_modaltableall" class="cbox" type="checkbox" aria-checked="false">'
            		));
            for (i = 0; i<labels.length; i++)
              tableheadercontent.append( $('<th/>').addClass('text-capitalize').text(gettext(labels[i])) );

            var tablebodycontent = $('<tbody/>');
            for (i = 0; i<data.length; i++) {
              var row = $('<tr/>');
              var td = $('<td/>');

              td.append( $('<input/>').attr({'id':"cb_modaltable-"+i, 'class':"cbox", 'type':"checkbox", 'aria-checked':"false"}));
              row.append(td);
              for (var j = 0; j < labels.length; j++)
                row.append( $('<td/>').text(data[i][labels[j]]) );
              tablebodycontent.append( row );
            };

          };

          $('#popup table').append(tablebodycontent);
          $('#popup thead').append(tableheadercontent);

          $('#popup').modal({backdrop: 'static', keyboard: false}).on('shown.bs.modal', function () {
            $(this).find('.modal-dialog').css({
              'max-width': 50+$('#forecastexporttable').width()+'px',
              'visibility': 'visible'
            });
          }).modal('show');

          $('#button_export').on('click', function() {
            //get selected row data
            data=[];
            var row1 = [];
            var row1data = {};
            var rows=$('#forecastexporttable tr.selected');

            $.each(rows, function( key, value ) {
              row1=value.children;
              row1data['id'] = row1[1].textContent;
              row1data['type'] = row1[2].textContent;
              row1data['item'] = row1[3].textContent;
              row1data['value'] = row1[4].textContent;
              row1data['quantity'] = row1[5].textContent;
              row1data['location'] = row1[6].textContent;
              row1data['origin'] = row1[7].textContent;
              row1data['startdate'] = row1[8].textContent;
              row1data['enddate'] = row1[9].textContent;
              row1data['criticality'] = row1[10].textContent;
              data.push(row1data);
            });

            $('#popup .modal-body').html(gettext('connecting') + '...');
            $.ajax({
              url: url_prefix + "/erp/upload/",
              data: JSON.stringify(data),
              type: "POST",
              contentType: "application/json",
              success: function () {
                $('#popup .modal-body').html(gettext("Export successful"));
                $('#cancelbutton').val(gettext('Close'));
                $('#button_export').toggleClass("btn-primary").prop('disabled', true );
                // Mark selected rows as "approved" if the original status was "proposed".
                for (var i in sel) {
                  var cur = grid.jqGrid('getCell', sel[i], 'status');
                  if (cur == 'proposed')
                    grid.jqGrid('setCell', sel[i], 'status', 'approved');
                };
              },
              error: function (result, stat, errorThrown) {
                $('#popup .modal-title').html(gettext("Error during export"));
                $('#popup .modal-header').addClass('bg-danger');
                $('#popup .modal-body').css({'overflow-y':'auto'}).html('<div style="overflow-y:auto; height: 300px; resize: vertical">' + result.responseText + '</div>');
                $('#button_export').val(gettext('Retry'));
                $('#popup .modal-dialog').css({'visibility':'visible'})
                $('#popup').modal('show');
              }
            });
          });

          $("#cb_modaltableall").click( function() {
            $("#forecastexporttable input[type=checkbox]").prop("checked", $(this).prop("checked"));
            $("#forecastexporttable tbody tr").toggleClass('selected');
            if ( $("#forecastexporttable tbody input[type=checkbox]:checked").length > 0 ) {
              $('#button_export').removeClass("active").addClass("active").prop('disabled', false );;
            } else {
              $('#button_export').removeClass("active").prop('disabled', true );
            };
          });
          $("#forecastexporttable tbody input[type=checkbox]").click( function() {
            $(this).parent().parent().toggleClass('selected');
            $("#cb_modaltableall").prop("checked",$("#forecastexporttable tbody input[type=checkbox]:not(:checked)").length == 0);
            if ( $("#forecastexporttable tbody input[type=checkbox]:checked").length > 0 ) {
              $('#button_export').removeClass("active").addClass("active").prop('disabled', false );;
            } else {
              $('#button_export').removeClass("active").prop('disabled', true );
            };
          });
          if ($("#actions").length)
            $("#actions1 span").text($("#actionsul").children().first().text());
        },
        error: function (result, stat, errorThrown) {
          $('#popup .modal-title').html(gettext("Error"));
          $('#popup .modal-header').addClass('bg-danger');
          $('#popup .modal-body').css({'overflow-y':'auto'}).html('<div style="overflow-y:auto; height: 300px; resize: vertical">' + result.responseText + '</div>');
          $('#button_export').val(gettext('Retry'));
          $('#popup .modal-dialog').css({'visibility':'visible'})
          $('#popup').modal('show');
        }
      });

    }
} //end Code for ERP integration

//----------------------------------------------------------------------------
// Code for sending dashboard configuration to the server.
//----------------------------------------------------------------------------

var dashboard = {
  dragAndDrop: function() {

    $(".cockpitcolumn").each( function() {
      Sortable.create($(this)[ 0 ], {
        group: "widgets",
        handle: ".panel-heading",
        animation: 100,
        onEnd: function (e) { dashboard.save();}
      });
    });

    $("#dashboard").each( function() {
      Sortable.create($(this)[ 0 ], {
        group: "cockpit",
        handle: "h1",
        animation: 100,
        onEnd: function (e) { dashboard.save();}
      });
    });

    $(".panel-toggle").click(function() {
      var icon = $(this);
      icon.toggleClass("fa-minus fa-plus");
      icon.closest(".panel").find(".panel-body").toggle();
      });
    $(".panel-close").click(function() {
      $(this).closest(".panel").remove();
      dashboard.save();
      });
  },

  save : function(reload)
  {
    // Loop over all rows
    var results = [];
    $("[data-cockpit-row]").each(function() {
      var rowname = $(this).attr("data-cockpit-row");
      var cols = [];
      // Loop over all columns in the row
      $(".cockpitcolumn", this).each(function() {
        var width = 12;
        if ($(this).hasClass("col-md-12"))
          width = 12;
        else if ($(this).hasClass("col-md-11"))
          width = 11;
        else if ($(this).hasClass("col-md-10"))
          width = 10;
        else if ($(this).hasClass("col-md-9"))
          width = 9;
        else if ($(this).hasClass("col-md-8"))
          width = 8;
        else if ($(this).hasClass("col-md-7"))
          width = 7;
        else if ($(this).hasClass("col-md-6"))
          width = 6;
        else if ($(this).hasClass("col-md-5"))
          width = 5;
        else if ($(this).hasClass("col-md-4"))
          width = 4;
        else if ($(this).hasClass("col-md-3"))
          width = 3;
        else if ($(this).hasClass("col-md-2"))
          width = 2;
        // Loop over all widgets in the column
        var widgets = [];
        $("[data-cockpit-widget]", this).each(function() {
          widgets.push( [$(this).attr("data-cockpit-widget"),{}] );
        });
        cols.push( {'width': width, 'widgets': widgets});
      });
      if (cols.length > 0)
        results.push( {'rowname': rowname, 'cols': cols});
    });

    // Send to the server
    if (typeof url_prefix != 'undefined')
        var url = url_prefix + '/settings/';
      else
        var url = '/settings/';
    $.ajax({
      url: url,
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({"freppledb.common.cockpit": results}),
      success: function () {
        if ($.type(reload) === "string")
          window.location.href = window.location.href;
      },
      error: ajaxerror
      });
  },

  customize: function(rowname)
  {
    // Detect the current layout of this row
    var layout = "";
    $("[data-cockpit-row='" + rowname + "'] .cockpitcolumn").each(function() {
      if (layout != "")
        layout += " - ";
      if ($(this).hasClass("col-md-12"))
        layout += "100%";
      else if ($(this).hasClass("col-md-11"))
        layout += "92%";
      else if ($(this).hasClass("col-md-10"))
        layout += "83%";
      else if ($(this).hasClass("col-md-9"))
        layout += "75%";
      else if ($(this).hasClass("col-md-8"))
        layout += "67%";
      else if ($(this).hasClass("col-md-7"))
        layout += "58%";
      else if ($(this).hasClass("col-md-6"))
        layout += "50%";
      else if ($(this).hasClass("col-md-5"))
        layout += "42%";
      else if ($(this).hasClass("col-md-4"))
        layout += "33%";
      else if ($(this).hasClass("col-md-3"))
        layout += "25%";
      else if ($(this).hasClass("col-md-2"))
        layout += "17%";
      });

    var txt = '<div class="modal-dialog">' +
      '<div class="modal-content">' +
        '<div class="modal-header">' +
          '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>' +
          '<h4 class="modal-title">' + gettext("Customize a dashboard row") + '</h4>' +
        '</div>' +
      '<div class="modal-body">' +
        '<form class="form-horizontal">' +

         '<div class="form-group">' +
       '<label class="col-md-3 control-label" for="id_name">' + gettext("Name") + ':</label>' +
       '<div class="col-md-9">' +
       '<input id="id_name" class="form-control" type="text" value="' + rowname + '">' +
         '</div></div>' +

         '<div class="form-group">' +
       '<label class="col-md-3 control-label" for="id_layout2">' + gettext("Layout") + ':</label>' +
       '<div class="col-md-9 dropdown dropdown-submit-input">' +
     '<button class="btn btn-default dropdown-toggle" id="id_layout2" name="layout" type="button" data-toggle="dropdown" aria-haspopup="true">' +
       '<span id="id_layout">' + layout + '</span>&nbsp;<span class="caret"></span>' +
     '</button>' +
     '<ul class="dropdown-menu" aria-labelledby="id_layout" id="id_layoutul">' +
     '<li class="dropdown-header">' + gettext("Single column") + '</li>' +
     '<li><a onclick="dashboard.setlayout(this)">100%</a></li>' +
     '<li class="divider"></li>' +
     '<li class="dropdown-header">' + gettext("Two columns") + '</li>' +
     '<li><a onclick="dashboard.setlayout(this)">75% - 25%</a></li>' +
     '<li><a onclick="dashboard.setlayout(this)">67% - 33%</a></li>' +
     '<li><a onclick="dashboard.setlayout(this)">50% - 50%</a></li>' +
     '<li><a onclick="dashboard.setlayout(this)">33% - 67%</a></li>' +
     '<li><a onclick="dashboard.setlayout(this)">25% - 75%</a></li>' +
     '<li class="divider"></li>' +
     '<li class="dropdown-header">' + gettext("Three columns") + '</li>' +
     '<li><a onclick="dashboard.setlayout(this)">50% - 25% - 25%</a></li>' +
     '<li><a onclick="dashboard.setlayout(this)">33% - 33% - 33%</a></li>' +
     '<li class="divider"></li>' +
     '<li class="dropdown-header">' + gettext("Four columns") + '</li>' +
     '<li><a onclick="dashboard.setlayout(this)">25% - 25% - 25% - 25%</a></li>' +
     '</ul></div>' +
       '</div>' +

         '<div class="form-group">' +
       '<label class="col-md-3 control-label" for="id_widget2">' + gettext("Add widget") + ':</label>' +
       '<div class="col-md-9 dropdown dropdown-submit-input">' +
     '<button class="btn btn-default dropdown-toggle" id="id_widget2" type="button" data-toggle="dropdown">' +
     '<span id="id_widget">-</span>&nbsp;<span class="caret"></span>' +
     '</button>' +
     '<ul class="dropdown-menu col-sm-9" aria-labelledby="id_widget2" id="id_widgetul">';

       var numwidgets = hiddenwidgets.length;
       for (var i = 0; i < numwidgets; i++)
         txt += '<li><a onclick="dashboard.setwidget(' + i + ')">' + hiddenwidgets[i][1] + '</a></li>';

       txt +=
     '</ul></div><span id="newwidgetname" style="display:none"></span>' +
       '</div>' +

     '</form></div>' +
     '<div class="modal-footer">' +
     '<input type="submit" role="button" onclick=\'$("#popup").modal("hide")\' class="btn btn-primary pull-left" data-dismiss="modal" value="' + gettext('Cancel') + '">' +
     '<input type="submit" role="button" onclick=\'dashboard.saveCustomization("' + rowname + '")\' class="btn btn-primary pull-right" value="' + gettext('Save') + '">' +
     '<input type="submit" role="button" onclick=\'dashboard.addRow("' + rowname + '", false)\' class="btn btn-primary pull-right" value="' + gettext('Add new below') + '">' +
     '<input type="submit" role="button" onclick=\'dashboard.addRow("' + rowname + '", true)\' class="btn btn-primary pull-right" value="' + gettext('Add new above') + '">' +
     '<input type="submit" role="button" onclick=\'dashboard.deleteRow("' + rowname + '")\' class="btn btn-primary pull-right" value="' + gettext('Delete') + '">' +
     '</div>' +

     '</div></div></div>';

      $('#popup').html(txt).modal('show');
  },

  setlayout: function(elem) {
    $("#id_layout").text($(elem).text());
  },

  setwidget: function(idx) {
    $("#id_widget").text(hiddenwidgets[idx][1]);
    $("#newwidgetname").text(hiddenwidgets[idx][0]);
  },

  saveCustomization: function(rowname) {
	// Update the name
    var newname = $("#id_name").val();
    if (rowname != newname)
    {
      // Make sure name is unique
      var cnt = 2;
      while ($("[data-cockpit-row='" + newname + "']").length > 1)
        newname = $("#id_name").val() + ' - ' + (cnt++);

      // Update
      $("[data-cockpit-row='" + rowname + "'] .col-md-11 h1").text(newname);
      $("[data-cockpit-row='" + rowname + "'] h1 button").attr("onclick", "dashboard.customize('" + newname + "')");
      $("[data-cockpit-row='" + rowname + "'] .horizontal-form").attr("id", newname);
      $("[data-cockpit-row='" + rowname + "']").attr("data-cockpit-row", newname);
    }

    // Update the layout
    var newlayout = $("#id_layout").text().split("-");
    var colindex = 0;
    var lastcol = null;
    // Loop over existing columns
    $("[id='" + rowname + "'] .cockpitcolumn").each(function() {
      if (colindex < newlayout.length)
      {
        // Resize existing column
        lastcol = this;
        $(this).removeClass("col-md-1 col-md-2 col-md-3 col-md-4 col-md-5 col-md-6 col-md-7 col-md-8 col-md-9 col-md-10 col-md-11 col-md-12");
        $(this).addClass("col-md-" + Math.round(0.12 * parseInt(newlayout[colindex])));
      }
      else
      {
        // Remove this column, after moving all widgets to the previous column
        $("[data-cockpit-widget]", this).appendTo(lastcol);
        $(this).remove();
      }
      colindex++;
    });
    while(colindex < newlayout.length)
    {
      // Adding extra columns
      lastcol = $('<div class="cockpitcolumn col-md-' + Math.round(0.12 * parseInt(newlayout[colindex])) + ' col-sm-12"></div>').insertAfter(lastcol);
      colindex++;
    }

    // Adding new widget
    var newwidget = $("#newwidgetname").text();
    if (newwidget != '') {
      $('<div class="panel panel-default"></div>').attr("data-cockpit-widget", newwidget).appendTo(lastcol);
      dashboard.save("true"); // Force reload of the page
    }
    else
      dashboard.save();

    // Almost done
    dashboard.dragAndDrop();
    $('#popup').modal('hide');
  },

  deleteRow: function(rowname) {
    $("[data-cockpit-row='" + rowname + "']").remove();
    dashboard.save();
    $('#popup').modal('hide');
  },

  addRow: function(rowname, position_above) {
	// Make sure name is unique
	var newname = $("#id_name").val();
	var cnt = 2;
	while ($("[data-cockpit-row='" + newname + "']").length >= 1)
      newname = $("#id_name").val() + ' - ' + (cnt++);

    // Build new content
    var newelements = '<div class="row" data-cockpit-row="' + newname + '">' +
      '<div class="col-md-11"><h1 style="float: left">' + newname + '</h1></div>' +
      '<div class="col-md-1"><h1 class="pull-right">' +
        '<button class="btn btn-xs btn-primary" onclick="dashboard.customize(\'' + newname + '\')" data-toggle="tooltip" data-placement="top" data-original-title="' + gettext("Customize") + '"><span class="fa fa-wrench"></span></button>' +
      '</h1></div>' +

      '<div class="horizontal-form" id="' + newname + '">';
    var newlayout = $("#id_layout").text().split("-");
    var newwidget = $("#newwidgetname").text();
    for (var i = 0; i < newlayout.length; i++)
    {
      newelements += '<div class="cockpitcolumn col-md-' + Math.round(0.12 * parseInt(newlayout[i])) + ' col-sm-12">';
      if (i == 0 && newwidget != '')
        newelements += '<div class="panel panel-default" data-cockpit-widget="' + newwidget + '"></div>';
      newelements += '</div>';
    }
    newelements += '</div></div></div>';

    // Insert in page
    if (position_above)
      $.find("[data-cockpit-row='" + rowname + "']").first().before($(newelements));
    else
      $.find("[data-cockpit-row='" + rowname + "']").last().after($(newelements));

    // Almost done
    if (newwidget != '')
      // Force reload of the page when adding a widget
      dashboard.save("true");
    else
      dashboard.save();
    dashboard.dragAndDrop();
    $('#popup').modal('hide');
  }

}


function savePreference(setting, value, callback) {
  if (typeof url_prefix != 'undefined')
    var url = url_prefix + '/settings/';
  else
    var url = '/settings/';
  var data = {};
  data[setting] = value;
  $.ajax({
    url: url,
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function() {
      if (typeof callback === 'function')
      	callback();
    }
  });
}

function getUnreadMessages() {
  $.ajax({
      url: url_prefix + "/inbox/",
      type: "GET",
      contentType: "application/json",
      success: function (json) {
        var msg = $("#messages");
        if (json.unread) {
          msg.removeClass("fa-envelope-open-o").addClass("fa-envelope-o");
          msg.next().text(json.unread);
          msg.parent().parent().attr("data-original-title", interpolate(gettext("%s unread messages"), [json.unread]));
        }
        else {
          msg.removeClass("fa-envelope-o").addClass("fa-envelope-open-o");
          msg.next().text("");
          msg.parent().parent().attr("data-original-title", gettext("No unread messages"));
        }
      }
   }); 
}

$(function() {

  // Send django's CRSF token with every POST request to the same site
  $(document).ajaxSend(function(event, xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && sameOrigin(settings.url))
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    });

  // Never cache ajax results
  $.ajaxSetup({ cache: false });

  getUnreadMessages();
  
  // Autocomplete search functionality
  var searchsource = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    //prefetch: '/search/',
    remote: {
      url: url_prefix + '/search/?term=%QUERY',
      wildcard: '%QUERY'
    }
  });
  $('#search').typeahead({minLength: 2}, {
    limit:1000,
    highlight: true,
    name: 'search',
    display: 'value',
    source: searchsource,
    templates: {
      suggestion: function(data){
        if (data.value === null)
          return '<span><p style="margin-top: 5px; margin-bottom: 1px;">' 
            + $.jgrid.htmlEncode(data.label) 
            + '</p><li  role="separator" class="divider"></li></span>';
        var href = url_prefix + data.url + admin_escape(data.value);
        if (!data.removeTrailingSlash) href += "/?noautofilter"; 
        return '<li><a href="'+ href + '" >' 
            + $.jgrid.htmlEncode(data.display) 
            + '</a><div class="tt-external"><a target="_blank" href="' + href + '">'
            + '<i class="fa fa-external-link" aria-hidden="true"></i>'
            + '</a></div></li>';
      },
    }
  });

});


//----------------------------------------------------------------------------
// Cookie manipulation functions
//----------------------------------------------------------------------------

function getCookie(name) {
  var allcookies = document.cookie.split(';');
  var search = name + '=';
  for (var i = allcookies.length; i >= 0; i--)
    if (jQuery.trim(allcookies[i]).indexOf(search) == 0)
      return jQuery.trim(allcookies[i]).substr(search.length);
  return null;
}

function setCookie(name, value, days) {
	// When the expiry is unspecified, you get a cookie valid for the browser session
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}


//----------------------------------------------------------------------------
// Check whether a URL is on the same domain as the current location or not.
// We use it to avoid send the CSRF-token to ajax requests submitted to other
// sites - for security reasons.
//----------------------------------------------------------------------------

function sameOrigin(url) {
    // URL could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

//----------------------------------------------------------------------------
//Display About dialog
//----------------------------------------------------------------------------

function about_show()
{

  $.ajax({
    url: "/about/",
    type: "GET",
    contentType: "application/json",
    success: function (data) {
      $('#timebuckets').modal('hide');
      $.jgrid.hideModal("#searchmodfbox_grid");
      $('#popup').modal({keyboard: false, backdrop:'static'});
      var version = data.version.split(".");
      var website = data.website;
      var content = '<div class="modal-dialog" style="width: 450px;">'+
         '<div class="modal-content">'+
           '<div class="modal-header">'+
             '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>'+
             '<h4 class="modal-title">About frePPLe ' + data.version + ' Community Edition</h4>'+
           '</div>'+
           '<div class="modal-body">'+
             '<div class="row">';
      content += '<div class="col-sm-5"><br><br>' +
         '<p><a target="_blank" href="' + website + '"><strong>frePPLe website &nbsp;<span class="fa fa-caret-right"></span></strong></a></p><br>' +
         '<p><a target="_blank" href="' + website + '/docs/' + version[0] + '.' + version[1] + '/license.html"><strong>License information &nbsp;<span class="fa fa-caret-right"></span></strong></a></p><br>' +
         '<p><a target="_blank" href="' + website + '/docs/' + version[0] + '.' + version[1] + '/index.html"><strong>Documentation &nbsp;<span class="fa fa-caret-right"></span></strong></a></p>' +
         '</div>' +
         '<div class="col-sm-7"><strong>' + gettext("Installed apps") + ":</strong>";
      for (var i in data.apps)
          content += '<br>&nbsp;&nbsp;' + data.apps[i];
      content += '</div>' +
             '</div>'+
           '</div>'+
         '</div>'+
       '</div>';
       $('#popup').html(content).modal('show');
      },
    error: ajaxerror
  });
}
//----------------------------------------------------------------------------
// Display import dialog for CSV-files
//----------------------------------------------------------------------------

function import_show(title, paragraph, multiple, fxhr, initialDropped)
{
  var xhr = {abort: function () {}};

  $('#timebuckets').modal('hide');
  $.jgrid.hideModal("#searchmodfbox_grid");
  $('#popup').modal({keyboard: false, backdrop:'static'});
  var modalcontent = '<div class="modal-dialog">'+
      '<div class="modal-content">'+
        '<div class="modal-header">'+
          '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" class="fa fa-times"></span></button>'+
          '<h4 class="modal-title">'+
            '<span id="modal_title">'+gettext("Import CSV or Excel file")+ '</span>' +'&nbsp;'+
            '<span id="animatedcog" class="fa fa-cog fa-spin fa-2x fa-fw" style="visibility: hidden;"></span>'+
          '</h4>'+
        '</div>'+
        '<div class="modal-body">'+
          '<form id="uploadform">' +
            '<p id="extra_text">'+gettext('Load an Excel file or a CSV-formatted text file.') + '<br>' +
              gettext('The first row should contain the field names.') + '<br><br>' +
              '<input type="checkbox" autocomplete="off" name="erase" value="yes"/>&nbsp;&nbsp;'+
              gettext('First delete all existing records AND ALL RELATED TABLES') + '<br><br>' +
            '</p>';
    if (isDragnDropUploadCapable()) {
      modalcontent += ''+
            '<div class="box" style="outline: 2px dashed black; outline-offset: -10px">'+
              '<div class="box__input" style="text-align: center; padding: 20px;">'+
                '<i class="fa fa-sign-in fa-5x fa-rotate-90"></i>'+
                '<input class="box__file invisible" type="file" id="csv_file" name="csv_file" data-multiple-caption="{count} '+gettext("files selected")+'" multiple/>'+
                '<label id="uploadlabel" for="csv_file">'+
                  '<kbd>'+
                    gettext('Select files')+
                  '</kbd>&nbsp;'+
                  '<span class="box__dragndrop" style="display: inline;">'+
                    gettext('or drop them here')+
                  '</span>.'+
                '</label>'+
              '</div>'+
              '<div class="box__uploading" style="display: none;">Uploading&hellip;</div>'+
              '<div class="box__success" style="display: none;">Done!</div>'+
              '<div class="box__error" style="display: none;">Error!<span></span>.</div>'+
            '</div>';
    } else {
      modalcontent += gettext('Data file') + ':<input type="file" id="csv_file" name="csv_file"/>';
    }
    modalcontent += ''+
          '<br></form>' +
          '<div style="margin: 5px 0">'+
            '<div id="uploadResponse" style="height: 50vh; resize: vertical; display: none; background-color: inherit; border: none; overflow: auto;"></div>'+
          '</div>'+
        '</div>'+
        '<div class="modal-footer">'+
            '<input type="submit" id="importbutton" role="button" class="btn btn-primary pull-right" value="'+gettext('Import')+'">'+
            '<input type="submit" id="cancelimportbutton" role="button" class="btn btn-primary pull-left" value="'+gettext('Cancel Import')+'" style="display: none;">'+
            '<input type="submit" id="cancelbutton" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Close')+'">'+
            '<input type="submit" id="copytoclipboard" role="button" class="btn btn-primary pull-left" value="'+gettext('Copy to Clipboard')+'" style="display: none;">' +
        '</div>'+
      '</div>'+
    '</div>';
  $('#popup').html(modalcontent).modal('show');

  if (!multiple) {
    $("#selected_files").removeAttr(multiple);
  }
  if (title !== '') {
    $("#modal_title").text(title);
  }
  if (paragraph === null) {
    $("#extra_text").remove();
  } else if (paragraph !== '') {
    $("#extra_text").text(paragraph);
  }

  var filesdropped = false;
  var filesselected = false;
  if (isDragnDropUploadCapable()) {
    $('.box').on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
    })
    .on('dragover dragenter', function() {
      $('.box').removeClass('bg-warning').addClass('bg-warning');
    })
    .on('dragleave dragend drop', function() {
      $('.box').removeClass('bg-warning');
    })
    .on('drop', function(e) {
      if (multiple)
        filesdropped = e.originalEvent.dataTransfer.files;
      else
        filesdropped = [e.originalEvent.dataTransfer.files[0]];
      $("#uploadlabel").text(filesdropped.length > 1 ? ($("#csv_file").attr('data-multiple-caption') || '').replace( '{count}', filesdropped.length ) : filesdropped[ 0 ].name);
    });
  }
  $("#csv_file").on('change', function(e) {
    if (multiple)
      filesselected = e.target.files;
    else
      filesselected = [e.target.files[0]];
    $("#uploadlabel").text(filesselected.length > 1 ? ($("#csv_file").attr('data-multiple-caption') || '').replace( '{count}', filesselected.length ) : filesselected[ 0 ].name);
    });
  if (initialDropped !== null && typeof initialDropped !== 'undefined') {
    if (multiple)
      filesdropped = initialDropped;
    else
      filesdropped = [initialDropped[0]];  	
  	$("#uploadlabel").text(
      filesdropped.length > 1 ?
      ($("#csv_file").attr('data-multiple-caption') || '').replace( '{count}', filesdropped.length ) : 
      filesdropped[0].name
      );
  };
  $('#importbutton').on('click', function() {
    if ($("#csv_file").val() === "" && !filesdropped) {
      return;
    }
    var filesdata = '';

    $('#uploadResponse').css('display','block');
    $('#uploadResponse').html(gettext('Importing...'));
    $('#uploadResponse').on('scroll', function() {
      if( parseInt($('#uploadResponse').attr('data-scrolled')) !== $('#uploadResponse').scrollTop() ) {
        $('#uploadResponse').attr('data-scrolled',true);
        $('#uploadResponse').off('scroll');
      }
    });
    $('#importbutton').hide();
    $("#animatedcog").css('visibility','visible');
    $('#uploadform').css('display','none');
    $('#copytoclipboard').on('click', function() {
      var sometextcontent = document.createRange();
      sometextcontent.selectNode(document.getElementById("uploadResponse"));
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(sometextcontent);
      document.execCommand('copy');
    });
    $('#cancelimportbutton').show().on('click', function() {
      var theclone = $("#uploadResponse").clone();
      theclone.append('<div><strong>'+gettext('Canceled')+'</strong></div>');
      xhr.abort();
      $("#animatedcog").css('visibility','hidden');
      $("#uploadResponse").append(theclone.contents());
      $("#uploadResponse").scrollTop($("#uploadResponse")[0].scrollHeight);
      $('#cancelimportbutton').hide();
      $('#copytoclipboard').show();
    });

    // Empty the csv-file field
    //$("#csv_file").wrap('<form>').closest('form').get(0).reset();
    //$("#csv_file").unwrap();
    
    // Prepare formdata
    filesdata = new FormData($("#uploadform")[0]);
    if (filesdropped) {
      $.each( filesdropped, function(i, fdropped) {
        filesdata.append( fdropped.name, fdropped );
      });
    }
    if (filesselected) {
    	filesdata.delete('csv_file');
      $.each( filesselected, function(i, fdropped) {
        filesdata.append( fdropped.name, fdropped );
      });      
    }
    
    // Upload the files
    xhr = $.ajax(
      Object.assign({
        type: 'post',
        url: typeof(url) != 'undefined' ? url : '',
        cache: false,
        data: filesdata,
        success: function (data) {
          var el = $('#uploadResponse');
          el.html(data);
          if (el.attr('data-scrolled') !== "true") {
            el.scrollTop(el[0].scrollHeight - el.height());
          }
          $('#cancelbutton').html(gettext('Close'));
          $('#importbutton').hide();
          $("#animatedcog").css('visibility','hidden');
          $('#cancelimportbutton').hide();
          if (document.queryCommandSupported('copy')) {
            $('#copytoclipboard').show();
          }
          $("#grid").trigger("reloadGrid");
        },
        xhrFields: {
          onprogress: function (e) {
            var el = $('#uploadResponse');
            el.html(e.currentTarget.response);
            var progress = el.find(".recordcount").last();
            var records = el.find("[data-cnt]").last().attr("data-cnt");
            progress.text(interpolate(gettext("%s records processed"), [records]));
            if (el.attr('data-scrolled')!== "true") {
              el.attr('data-scrolled', el[0].scrollHeight - el.height());
              el.scrollTop(el[0].scrollHeight - el.height());
            }
          }
        },
        error: function() {
          $('#cancelimportbutton').hide();
          $('#copytoclipboard').show();
          $("#animatedcog").css('visibility','hidden');
          $("#uploadResponse").scrollTop($("#uploadResponse")[0].scrollHeight);
        },
        processData: false,
        contentType: false
      }, fxhr)
    );
   }
  );
}


//----------------------------------------------------------------------------
// This function returns all arguments in the current URL as a dictionary.
//----------------------------------------------------------------------------

function getURLparameters()
{

  if (window.location.search.length == 0) return {};
  var params = {};
  jQuery.each(window.location.search.match(/^\??(.*)$/)[1].split('&'), function(i,p){
    p = p.split('=');
    p[1] = unescape(p[1]).replace(/\+/g,' ');
    params[p[0]] = params[p[0]]?((params[p[0]] instanceof Array)?(params[p[0]].push(p[1]),params[p[0]]):[params[p[0]],p[1]]):p[1];
  });
  return params;
};


//----------------------------------------------------------------------------
// Dropdown list to select the model.
//----------------------------------------------------------------------------

function selectDatabase()
{
  // Find new database and current database
  var db = $(this).attr("data-database");

  // Change the location
  if (database == db)
    return;
  else if (database == 'default')
  {
    if (window.location.pathname == '/')
      window.location.href = "/" + db + "/";
    else
      window.location.href = window.location.href.replace(window.location.pathname, "/" + db + window.location.pathname);
  }
  else if (db == 'default')
    window.location.href = window.location.href.replace("/"+database+"/", "/");
  else
    window.location.href = window.location.href.replace("/"+database+"/", "/" + db + "/");
};


//----------------------------------------------------------------------------
// Jquery utility function to bind an event such that it fires first.
//----------------------------------------------------------------------------

$.fn.bindFirst = function(name, fn) {
  // bind as you normally would
  // don't want to miss out on any jQuery magic
  this.on(name, fn);

  // Thanks to a comment by @Martin, adding support for
  // namespaced events too.
  this.each(function() {
    var handlers = $._data(this, 'events')[name.split('.')[0]];
    // take out the handler we just inserted from the end
    var handler = handlers.pop();
    // move it at the beginning
    handlers.splice(0, 0, handler);
  });
};


//
// Graph functions
//

var graph = {

  header: function(margin, scale)
  {
    var el = $("#grid_graph");
    el.html("");
    var scale_stops = scale.range();
    var scale_width = scale.rangeBand();
    var svg = d3.select(el.get(0)).append("svg");
    svg.attr('height','15px');
    svg.attr('width', el.width());    
    var wt = 0;
    for (var i in timebuckets)
    { 
    	var w = margin + scale_stops[i] + scale_width / 2;
      if (wt <= w)
      {
        var t = svg.append('text')
          .attr('class',timebuckets[i]['history'] ? 'svgheaderhistory' : 'svgheadertext')
          .attr('x', w)
          .attr('y', '12')
          .text(timebuckets[i]['name']);
        wt = w + t.node().getComputedTextLength() + 12;
      }
    }
  },

  showTooltip: function(txt)
  {
    // Find or create the tooltip div
    var tt = d3.select("#tooltip");
    if (tt.empty())
      tt = d3.select("body")
        .append("div")
        .attr("id", "tooltip")
        .attr("role", "tooltip")
        .attr("class", "popover fade right in")
        .style("position", "absolute");

    // Update content and display
    tt.html('' + txt)
      .style('display', 'block');
    graph.moveTooltip();
  },

  hideTooltip: function()
  {
    d3.select("#tooltip").style('display', 'none');
    d3.event.stopPropagation();
  },

  moveTooltip: function()
  {
    var xpos = d3.event.pageX + 5;
    var ypos = d3.event.pageY - 28;
    var xlimit = $(window).width() - $("#tooltip").width() - 20;
    var ylimit = $(window).height() - $("#tooltip").height() - 20;
    if (xpos > xlimit)
    {
      // Display tooltip under the mouse
      xpos = xlimit;
      ypos = d3.event.pageY + 5;
    }
    if (ypos > ylimit)
      // Display tooltip above the mouse
      ypos = d3.event.pageY - $("#tooltip").height() - 25;
    d3.select("#tooltip")
      .style({
        'left': xpos + "px",
        'top': ypos + "px"
        });
    d3.event.stopPropagation();
  },

  miniAxis: function(s)
  {
    var sc = this.scale().range();
    var dm = this.scale().domain();
    // Draw the scale line
    s.append("path")
     .attr("class", "domain")
     .attr("d", "M-10 0 H0 V" + (sc[0]-2) + " H-10");
    // Draw the maximum value
    s.append("text")
     .attr("x", -2)
     .attr("y", 13) // Depends on font size...
     .attr("text-anchor", "end")
     .text(grid.formatNumber(Math.round(dm[1])));
    // Draw the minimum value
    s.append("text")
    .attr("x", -2)
    .attr("y", sc[0] - 5)
    .attr("text-anchor", "end")
    .text(Math.round(dm[0], 0));
  }
};

//
// Gantt chart functions
//

var gantt = {

  // Height of the blocks
  rowsize: 25,

  header : function ()
  {
    // "scaling" stores the number of pixels available to show a day.
  	var d = (viewend.getTime() - viewstart.getTime());
    var scaling = 86400000 / d * $("#jqgh_grid_operationplans").width();
    var total = (horizonend.getTime() - horizonstart.getTime()) / d * $("#jqgh_grid_operationplans").width();
    var result = [
      '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="' + total + 'px" height="34px">',
      '<line class="time" x1="0" y1="17" x2="' + total + '" y2="17"/>'
      ];
    var x = 0;
    if (scaling < 5)
    {
      // Quarterly + monthly buckets
      var bucketstart = new Date(horizonstart.getFullYear(), horizonstart.getMonth(), 1);
      while (bucketstart < horizonend)
      {
        var x1 = (bucketstart.getTime() - viewstart.getTime()) / 86400000 * scaling;
        var bucketend = new Date(bucketstart.getFullYear(), bucketstart.getMonth()+1, 1);
        var x2 = (bucketend.getTime() - viewstart.getTime()) / 86400000 * scaling;
        result.push('<text class="svgheadertext" x="' + Math.floor((x1+x2)/2) + '" y="31">' + moment(bucketstart).format("MMM") + '</text>');
        if (bucketstart.getMonth() % 3 == 0)
        {
          var quarterend = new Date(bucketstart.getFullYear(), bucketstart.getMonth()+3, 1);
          x2 = (quarterend.getTime() - viewstart.getTime()) / 86400000 * scaling;
          var quarter = Math.floor((bucketstart.getMonth()+3)/3);
          result.push('<line class="time" x1="' + Math.floor(x1) + '" y1="0" x2="' + Math.floor(x1) + '" y2="34"/>');
          result.push('<text class="svgheadertext" x="' + Math.floor((x1+x2)/2) + '" y="13">' + bucketstart.getFullYear() + " Q" + quarter + '</text>');
        }
        else
          result.push('<line class="time" x1="' + Math.floor(x1) + '" y1="17" x2="' + Math.floor(x1) + '" y2="34"/>');
        bucketstart = bucketend;
      }
    }
    else if (scaling < 10)
    {
      // Monthly + weekly buckets, short style
      x -= horizonstart.getDay() * scaling;
      var bucketstart = new Date(horizonstart.getTime() - 86400000 * viewstart.getDay());
      while (bucketstart < horizonend)
      {
        result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling*3.5) + '" y="31">' + moment(bucketstart).format("MM-DD") + '</text>');
        x = x + scaling*7;
        bucketstart.setTime(bucketstart.getTime() + 86400000 * 7);
      }
      bucketstart = new Date(horizonstart.getFullYear(), horizonstart.getMonth(), 1);
      while (bucketstart < horizonend)
      {
        x1 = (bucketstart.getTime() - viewstart.getTime()) / 86400000 * scaling;
        bucketend = new Date(bucketstart.getFullYear(), bucketstart.getMonth()+1, 1);
        x2 = (bucketend.getTime() - viewstart.getTime()) / 86400000 * scaling;
        result.push('<line class="time" x1="' + Math.floor(x1) + '" y1="0" x2="' + Math.floor(x1) + '" y2="17"/>');
        result.push('<text class="svgheadertext" x="' + Math.floor((x1+x2)/2) + '" y="13">' + moment(bucketstart).format("MMM YY") + '</text>');
        bucketstart = bucketend;
      }
    }
    else if (scaling < 20)
    {
      // Monthly + weekly buckets, long style
      x -= horizonstart.getDay() * scaling;
      var bucketstart = new Date(horizonstart.getTime() - 86400000 * horizonstart.getDay());
      while (bucketstart < horizonend)
      {
        result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        result.push('<text class="svgheadertext" x="' + (x + scaling*7.0/2.0) + '" y="31">' + moment(bucketstart).format("YY-MM-DD") + '</text>');
        x = x + scaling*7.0;
        bucketstart.setTime(bucketstart.getTime() + 86400000 * 7);
      }
      bucketstart = new Date(horizonstart.getFullYear(), horizonstart.getMonth(), 1);
      while (bucketstart < horizonend)
      {
        x1 = (bucketstart.getTime() - viewstart.getTime()) / 86400000 * scaling;
        bucketend = new Date(bucketstart.getFullYear(), bucketstart.getMonth()+1, 1);
        x2 = (bucketend.getTime() - viewstart.getTime()) / 86400000 * scaling;
        result.push('<line class="time" x1="' + Math.floor(x1) + '" y1="0" x2="' + Math.floor(x1) + '" y2="17"/>');
        result.push('<text class="svgheadertext" x="' + Math.floor((x1+x2)/2) + '" y="13">' + moment(bucketstart).format("MMM YY") + '</text>');
        bucketstart = bucketend;
      }
    }
    else if (scaling <= 40)
    {
      // Weekly + daily buckets, short style
      var bucketstart = new Date(horizonstart.getTime());
      while (bucketstart < horizonend)
      {
        if (bucketstart.getDay() == 0)
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="0" x2="' + Math.floor(x) + '" y2="34"/>');
          result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling*7/2) + '" y="13">' + moment(bucketstart).format("YY-MM-DD") + '</text>');
        }
        else
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        }
        result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling/2) + '" y="31">' + moment(bucketstart).format("DD") + '</text>');
        x = x + scaling;
        bucketstart.setDate(bucketstart.getDate()+1);
      }
    }
    else if (scaling <= 75)
    {
      // Weekly + daily buckets, long style
      var bucketstart = new Date(horizonstart.getTime());
      while (bucketstart < horizonend)
      {
        if (bucketstart.getDay() == 0)
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="0" x2="' + Math.floor(x) + '" y2="34"/>');
          result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling*7/2) + '" y="13">' + moment(bucketstart).format("YY-MM-DD") + '</text>');
        }
        else
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        }
        result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling/2) + '" y="31">' + moment(bucketstart).format("DD MM") + '</text>');
        x = x + scaling;
        bucketstart.setDate(bucketstart.getDate()+1);
      }
    }
    else if (scaling < 350)
    {
      // Weekly + daily buckets, very long style
      var bucketstart = new Date(horizonstart.getTime());
      while (bucketstart < horizonend)
      {
        if (bucketstart.getDay() == 0)
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="0" x2="' + Math.floor(x) + '" y2="34"/>');
          result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling*3.5) + '" y="13">' + moment(bucketstart).format("YY-MM-DD") + '</text>');
        }
        else
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling/2) + '" y="31">' + moment(bucketstart).format("ddd DD MMM") + '</text>');
        x = x + scaling;
        bucketstart.setDate(bucketstart.getDate()+1);
      }
    }
    else
    {
      // Daily + hourly buckets
      var bucketstart = new Date(horizonstart.getTime());
      while (bucketstart < horizonend)
      {
        if (bucketstart.getHours() == 0)
        {
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="0" x2="' + Math.floor(x) + '" y2="34"/>');
          result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling/2) + '" y="13">' + moment(bucketstart).format("ddd YY-MM-DD") + '</text>');
        }
        else
          result.push('<line class="time" x1="' + Math.floor(x) + '" y1="17" x2="' + Math.floor(x) + '" y2="34"/>');
        result.push('<text class="svgheadertext" x="' + Math.floor(x + scaling/48) + '" y="31">' + bucketstart.getHours() + '</text>');
        x = x + scaling/24;
        bucketstart.setTime(bucketstart.getTime() + 3600000);
      }
    }
    result.push('</svg>');
    $("#jqgh_grid_operationplans").html(result.join(''));
  },

  redraw: function()
  {
    // Determine the conversion between svg units and the screen
    var scale = (horizonend.getTime() - horizonstart.getTime())
       / (viewend.getTime() - viewstart.getTime())
       * $("#jqgh_grid_operationplans").width() / 10000;
    $('.transformer').each(function() {
      var layers = $(this).attr("title");
      $(this).attr("transform", "scale(" + scale + ",1) translate(0," + ((layers-1)*gantt.rowsize+3) + ")");
      });
    gantt.header();
  },

  scroll: function(event) {
  	var zone = viewend.getTime() - viewstart.getTime();
    viewstart.setTime(
    		horizonstart.getTime() 
    		+ $(event.target).scrollLeft() / event.target.scrollWidth * (horizonend.getTime() - horizonstart.getTime()) 
    		);
    viewend.setTime(viewstart.getTime() + zone);
    // Determine the conversion between svg units and the screen
    var scale = (horizonend.getTime() - horizonstart.getTime()) / zone * $("#jqgh_grid_operationplans").width() / 10000;
    var offset = (horizonstart.getTime() - viewstart.getTime()) / (horizonend.getTime() - horizonstart.getTime()) * 10000;
    // Transform all svg elements
    $('.transformer').each(function() {
      var layers = $(this).attr("title");
      $(this).attr("transform", "scale(" + scale + ",1) translate(" + offset + "," + ((layers-1)*gantt.rowsize+3) + ")");
      });
  },
  
  zoom: function(zoom_in_or_out)
  {
    // Determine the window to be shown. Min = 1 day. Max = 3 years.
    var zone = (viewend.getTime() - viewstart.getTime()) * zoom_in_or_out;
    if (zone >= horizonend.getTime() - horizonstart.getTime()) {
    	viewstart.setTime(horizonstart.getTime());
    	viewend.setTime(horizonend.getTime());
    	zone = viewend.getTime() - viewstart.getTime();
    }
    else {
    	viewend.setTime(viewstart.getTime() + zone);
      if (viewend.getTime() > horizonend.getTime()) {
      	viewend.setTime(horizonend.getTime());
      	viewstart.setTime(viewend.getTime() - zone);
       }
    }
    // Determine the conversion between svg units and the screen
    var scale = (horizonend.getTime() - horizonstart.getTime()) / zone * $("#jqgh_grid_operationplans").width() / 10000;
    var offset = (horizonstart.getTime() - viewstart.getTime()) / (horizonend.getTime() - horizonstart.getTime()) * 10000;
    // Transform all svg elements
    $('.transformer').each(function() {
      var layers = $(this).attr("title");
      $(this).attr("transform", "scale(" + scale + ",1) translate(" + offset + "," + ((layers-1)*gantt.rowsize+3) + ")");
      });
    // Redraw the header
    gantt.header();
  }
}

// Gauge for widgets on dashboard
// Copied from https://gist.github.com/tomerd/1499279

function Gauge(placeholderName, configuration)
{
  this.placeholderName = placeholderName;

  var self = this; // for internal d3 functions

  this.configure = function(configuration)
  {
    this.config = configuration;

    this.config.size = this.config.size * 0.9;

    this.config.raduis = this.config.size * 0.97 / 2;
    this.config.cx = this.config.size / 2;
    this.config.cy = this.config.size / 2;

    this.config.min = undefined != configuration.min ? configuration.min : 0;
    this.config.max = undefined != configuration.max ? configuration.max : 100;
    this.config.range = this.config.max - this.config.min;

    this.config.majorTicks = configuration.majorTicks || 5;
    this.config.minorTicks = configuration.minorTicks || 2;

    this.config.greenColor  = configuration.greenColor || "#109618";
    this.config.yellowColor = configuration.yellowColor || "#FF9900";
    this.config.redColor  = configuration.redColor || "#DC3912";

    this.config.transitionDuration = configuration.transitionDuration || 500;
  }

  this.render = function()
  {
    this.body = d3.select("#" + this.placeholderName)
              .append("svg:svg")
              .attr("class", "gauge")
              .attr("width", this.config.size)
              .attr("height", this.config.size);

    this.body.append("svg:circle")
          .attr("cx", this.config.cx)
          .attr("cy", this.config.cy)
          .attr("r", this.config.raduis)
          .style("fill", "#ccc")
          .style("stroke", "#000")
          .style("stroke-width", "0.5px");

    this.body.append("svg:circle")
          .attr("cx", this.config.cx)
          .attr("cy", this.config.cy)
          .attr("r", 0.9 * this.config.raduis)
          .style("fill", "#fff")
          .style("stroke", "#e0e0e0")
          .style("stroke-width", "2px");

    for (var index in this.config.greenZones)
    {
      this.drawBand(this.config.greenZones[index].from, this.config.greenZones[index].to, self.config.greenColor);
    }

    for (var index in this.config.yellowZones)
    {
      this.drawBand(this.config.yellowZones[index].from, this.config.yellowZones[index].to, self.config.yellowColor);
    }

    for (var index in this.config.redZones)
    {
      this.drawBand(this.config.redZones[index].from, this.config.redZones[index].to, self.config.redColor);
    }

    if (undefined != this.config.label)
    {
      var fontSize = Math.round(this.config.size / 9);
      this.body.append("svg:text")
            .attr("x", this.config.cx)
            .attr("y", this.config.cy / 2 + fontSize / 2)
            .attr("dy", fontSize / 2)
            .attr("text-anchor", "middle")
            .text(this.config.label)
            .style("font-size", fontSize + "px")
            .style("fill", "#333")
            .style("stroke-width", "0px");
    }

    var fontSize = Math.round(this.config.size / 16);
    var majorDelta = this.config.range / (this.config.majorTicks - 1);
    for (var major = this.config.min; major <= this.config.max; major += majorDelta)
    {
      var minorDelta = majorDelta / this.config.minorTicks;
      for (var minor = major + minorDelta; minor < Math.min(major + majorDelta, this.config.max); minor += minorDelta)
      {
        var point1 = this.valueToPoint(minor, 0.75);
        var point2 = this.valueToPoint(minor, 0.85);

        this.body.append("svg:line")
              .attr("x1", point1.x)
              .attr("y1", point1.y)
              .attr("x2", point2.x)
              .attr("y2", point2.y)
              .style("stroke", "#666")
              .style("stroke-width", "1px");
      }

      var point1 = this.valueToPoint(major, 0.7);
      var point2 = this.valueToPoint(major, 0.85);

      this.body.append("svg:line")
            .attr("x1", point1.x)
            .attr("y1", point1.y)
            .attr("x2", point2.x)
            .attr("y2", point2.y)
            .style("stroke", "#333")
            .style("stroke-width", "2px");

      if (major == this.config.min || major == this.config.max)
      {
        var point = this.valueToPoint(major, 0.63);

        this.body.append("svg:text")
              .attr("x", point.x)
              .attr("y", point.y)
              .attr("dy", fontSize / 3)
              .attr("text-anchor", major == this.config.min ? "start" : "end")
              .text(major)
              .style("font-size", fontSize + "px")
              .style("fill", "#333")
              .style("stroke-width", "0px");
      }
    }

    var pointerContainer = this.body.append("svg:g").attr("class", "pointerContainer");

    var midValue = (this.config.min + this.config.max) / 2;

    var pointerPath = this.buildPointerPath(midValue);

    var pointerLine = d3.svg.line()
                  .x(function(d) { return d.x })
                  .y(function(d) { return d.y })
                  .interpolate("basis");

    pointerContainer.selectAll("path")
              .data([pointerPath])
              .enter()
                .append("svg:path")
                  .attr("d", pointerLine)
                  .style("fill", "#dc3912")
                  .style("stroke", "#c63310")
                  .style("fill-opacity", 0.7);

    pointerContainer.append("svg:circle")
              .attr("cx", this.config.cx)
              .attr("cy", this.config.cy)
              .attr("r", 0.12 * this.config.raduis)
              .style("fill", "#4684EE")
              .style("stroke", "#666")
              .style("opacity", 1);

    var fontSize = Math.round(this.config.size / 10);
    pointerContainer.selectAll("text")
              .data([midValue])
              .enter()
                .append("svg:text")
                  .attr("x", this.config.cx)
                  .attr("y", this.config.size - this.config.cy / 4 - fontSize)
                  .attr("dy", fontSize / 2)
                  .attr("text-anchor", "middle")
                  .style("font-size", fontSize + "px")
                  .style("fill", "#000")
                  .style("stroke-width", "0px");

    this.redraw(this.config.value, 0);
  }

  this.buildPointerPath = function(value)
  {
    var delta = this.config.range / 13;

    var head = valueToPoint(value, 0.85);
    var head1 = valueToPoint(value - delta, 0.12);
    var head2 = valueToPoint(value + delta, 0.12);

    var tailValue = value - (this.config.range * (1/(270/360)) / 2);
    var tail = valueToPoint(tailValue, 0.28);
    var tail1 = valueToPoint(tailValue - delta, 0.12);
    var tail2 = valueToPoint(tailValue + delta, 0.12);

    return [head, head1, tail2, tail, tail1, head2, head];

    function valueToPoint(value, factor)
    {
      var point = self.valueToPoint(value, factor);
      point.x -= self.config.cx;
      point.y -= self.config.cy;
      return point;
    }
  }

  this.drawBand = function(start, end, color)
  {
    if (0 >= end - start) return;

    this.body.append("svg:path")
          .style("fill", color)
          .attr("d", d3.svg.arc()
            .startAngle(this.valueToRadians(start))
            .endAngle(this.valueToRadians(end))
            .innerRadius(0.65 * this.config.raduis)
            .outerRadius(0.85 * this.config.raduis))
          .attr("transform", function() { return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(270)" });
  }

  this.redraw = function(value, transitionDuration)
  {
    var pointerContainer = this.body.select(".pointerContainer");

    pointerContainer.selectAll("text").text(Math.round(value));

    var pointer = pointerContainer.selectAll("path");
    pointer.transition()
          .duration(undefined != transitionDuration ? transitionDuration : this.config.transitionDuration)
          //.delay(0)
          //.ease("linear")
          //.attr("transform", function(d)
          .attrTween("transform", function()
          {
            var pointerValue = value;
            if (value > self.config.max) pointerValue = self.config.max + 0.02*self.config.range;
            else if (value < self.config.min) pointerValue = self.config.min - 0.02*self.config.range;
            var targetRotation = (self.valueToDegrees(pointerValue) - 90);
            var currentRotation = self._currentRotation || targetRotation;
            self._currentRotation = targetRotation;

            return function(step)
            {
              var rotation = currentRotation + (targetRotation-currentRotation)*step;
              return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(" + rotation + ")";
            }
          });
  }

  this.valueToDegrees = function(value)
  {
    // thanks @closealert
    //return value / this.config.range * 270 - 45;
    return value / this.config.range * 270 - (this.config.min / this.config.range * 270 + 45);
  }

  this.valueToRadians = function(value)
  {
    return this.valueToDegrees(value) * Math.PI / 180;
  }

  this.valueToPoint = function(value, factor)
  {
    return {  x: this.config.cx - this.config.raduis * factor * Math.cos(this.valueToRadians(value)),
          y: this.config.cy - this.config.raduis * factor * Math.sin(this.valueToRadians(value))    };
  }

  // initialization
  this.configure(configuration);
}


function showModalImage(event, title) {
	var popup = $('#popup');
	popup.html(
	  '<div class="modal-dialog modal-lg" style="margin-top: 20px; width:90%; margin-left: auto; margin-right: auto">'
    + '<div class="modal-content">'
    + '<div class="modal-header" style="border-top-left-radius: inherit; border-top-right-radius: inherit">'
    + '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'
    + '<h4 class="modal-title"></h4>'
    + '</div>'
    + '<div class="modal-body">'
    + '<img src="" style="width:100%">'
    + '</div>'
    + '</div>'
    + '</div>');
	popup.find("h4").text(title);
	popup.find("img").attr("src", $(event.target).attr("src"));
  popup.modal('show');
	event.preventDefault();
}

/* Jquery extension to make an element draggable. 
 * Copied from http://cssdeck.com/labs/wsse5ous
 */
$.fn.drags = function(opt) {

  opt = $.extend({handle:"",cursor:"move"}, opt);

  if(opt.handle === "") {
      var $el = this;
  } else {
      var $el = this.find(opt.handle);
  }

  return $el
    .css('cursor', opt.cursor)
    .on("mousedown", function(e) {
      if(opt.handle === "")
          var $drag = $(this).addClass('draggable');
      else
          var $drag = $(this).addClass('active-handle').parent().addClass('draggable');
      var z_idx = $drag.css('z-index'),
          drg_h = $drag.outerHeight(),
          drg_w = $drag.outerWidth(),
          pos_y = $drag.offset().top + drg_h - e.pageY,
          pos_x = $drag.offset().left + drg_w - e.pageX;
      $drag.css('z-index', 1000).parents().on("mousemove", function(e) {
          $('.draggable').offset({
              top:e.pageY + pos_y - drg_h,
              left:e.pageX + pos_x - drg_w
          }).on("mouseup", function() {
              $(this).removeClass('draggable').css('z-index', z_idx);
          });
      });
      e.preventDefault(); // disable selection
  }).on("mouseup", function() {
      if(opt.handle === "") {
          $(this).removeClass('draggable');
      } else {
          $(this).removeClass('active-handle').parent().removeClass('draggable');
      }
  });
}

//  Follower functions

var follow = {
  setMethod: function(el) {
     var me = $(el);
     me.closest(".dropdown").find(".followerspan").text(me.text());
     },
     
  get: function(event, el) {
     var t = $(el);
     event.preventDefault();
     $.ajax({
       url: url_prefix + "/follow/",
       data: {
         "object_pk": t.attr("data-pk"),
         "model": t.attr("data-model"),
         },
       type: "GET",
       contentType: "application/json; charset=utf-8",
       success: function (data) {
         // Show dialog with detailed follower info
         $('#timebuckets').modal('hide');
         $.jgrid.hideModal("#searchmodfbox_grid");
         var dlg = $(
           '<div class="modal-dialog"><div class="modal-content">'+
           '<div class="modal-header">'+
              '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true" class="fa fa-times"></span></button>'+
              '<h4 class="modal-title"></h4>'+
           '</div>'+
           '<div class="modal-body">'+
             '<table id="follower_key" style="width:100%">'+
               '<tr><th>'+gettext("Follow")+' '+
               '<span class="dropdown">'+
               '<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">'+
               '<span class="followerspan"></span>&nbsp;<span class="caret">'+
               '</button>'+
               '<ul class="dropdown-menu">'+
                  '<li><a href="#" onclick="follow.setMethod(this)">online</a></li>'+
                  '<li><a href="#" onclick="follow.setMethod(this)">email</a></li>'+
                  '</ul></span>'+
               '</th></tr><tr><td id="follower_models" style="vertical-align:top"></td></tr>'+
             '</table>'+
           '</div>'+
           '<div class="modal-footer">'+
              '<input type="submit" role="button" class="btn btn-primary pull-right" onclick="follow.post(event, this)" value="'+gettext('Update')+'">'+
              '<input type="submit" role="button" class="btn btn-primary pull-left" data-dismiss="modal" value="'+gettext('Close')+'">'+
           '</div>'+
           '</div></div>'
           );
         dlg.find(".modal-title")
           .text(interpolate(gettext("Manage notifications of %s"), [data.label + " " + data.object_pk], false));
         dlg.find(".followerspan").text(data.type);
         dlg.find("#follower_key")
           .attr("data-model", data.model)
           .attr("data-object_pk", data["object_pk"]);
         if (data.parents) {
           // You're already following it through another object
           for (var p of data.parents) {
              var e = $("<div style='margin-top:10px; margin-bottom:10px'>" + gettext("Following") + " " + p.model + " <a class='underline' target='_blank'></a></div>");
              e.find("a").attr("href", p.url).text(p.object_pk);
              e.find("a").append($("<i style='text-indent:0.5em' class='fa fa-external-link'></i>"));
              dlg.find("td").first().append(e);
           }
         }
         else if (data.models) {
           // You're directly following this object or not following it yet.
           for (var p of data.models) {
             var e = $("<div class='checkbox'><label>"
               + "<input type='checkbox'/><span class='text-capitalize'></span>"
               + "</label></div>"
               );
              e.find("span").text(p.label);
              e.find("input").attr("data-model", p.model);
              if (p.checked) e.find("input").attr("checked", "true");
              dlg.find("td").first().append(e);
           }
         }
         if (data.users) {
           var e = $("<th></th>");
           e.text(gettext("Add followers"));
           dlg.find("th").after(e);
           e = $("<td id='follower_users' style='vertical-align:top'></td>");
           for (var u of data.users) {
             var e2 = $("<div class='checkbox'><label>"
               + "<input type='checkbox'/><span class='followername'></span>"
               + "</label>&nbsp;&nbsp;"
               + '<span class="dropdown">'
               + '<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">'
               + '<span class="followerspan"></span>&nbsp;<span class="caret">'
               + '</button>'
               + '<ul class="dropdown-menu">'
               + '<li><a href="#" onclick="follow.setMethod(this)">online</a></li>'
               + '<li><a href="#" onclick="follow.setMethod(this)">email</a></li>'
               + '</ul></span>'
               + "</div>"
               );
             e2.find("input").attr("data-username", u.username);
             if (u.following != "no") e2.find("input").attr("checked", "true");
             e2.find(".followerspan").text(u.following == "email" ? "email" : "online");
             if (u.following == "indirect") {
               e2.find("input").attr("disabled", "disabled");
               e2.find(".dropdown").addClass("disabled");
             }
             e2.find("span.followername").text(u.username);
             e.append(e2);
           }
           dlg.find("td").after(e);
         }
         $('#popup').html(dlg).modal('show');
         },
       error: ajaxerror
       });
     },
   
   post: function() {  
     var dlg = $("#popup");
     var key = dlg.find("#follower_key");
     var data = {
          "object_pk": key.attr("data-object_pk"),
          "model": key.attr("data-model"),
          "type": dlg.find("#follower_key .followerspan").text(),
          "users": {},
          "models": []
          };
     dlg.find("#follower_users input:checked").each(function(){
       if ($(this).attr("disabled") != "disabled") 
         data["users"][$(this).attr("data-username")] = $(this).closest(".checkbox").find(".followerspan").text();
     });
     dlg.find("#follower_models input:checked").each(function(){
       data["models"].push($(this).attr("data-model"));
     });
     $.ajax({
       url: url_prefix + "/follow/",
       data: JSON.stringify([data]),
       type: "POST",
       contentType: "application/json",
       success: function () {
          $('#popup').modal("hide");
          },
       error: ajaxerror
       });
     }
}

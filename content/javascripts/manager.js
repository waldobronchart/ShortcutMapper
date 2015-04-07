var pageManager = new function PageManager() {

    selectedApp = sitedata_apps[0];
    selectedAppData = null;
    selectedVersion = null;
    selectedContext = null;
    selectedOS = null;
    selectedKeyboardType = null;

    minSearchLength = 2;
    maxSearchResults = 50;
    prevNumSearchResults = 0;
    selectedSearchResult = -1;
    selectedSearchShortcut = {
        context: null,
        key: null,
        shortcut: null
    };

    this.init = function() {
        var manager = this;

        // Get selected app name from window hash
        var hash = window.location.hash;
        if (hash.length > 1) {
            hash = hash.substring(1).toLowerCase();
            for (var i=0; i<sitedata_apps.length; i++) {
                var name = sitedata_apps[i].name;
                if (this._appNameToHash(name).toLowerCase() === hash) {
                    selectedApp = sitedata_apps[i];
                }
            }
        }

        // Find all elements we're going to be using a lot
        this.elemAppSelect = $("#application_select");
        this.elemVersionSelect = $("#version_select");
        this.elemContextSelect = $("#context_select");
        this.elemKeyboardTypeSelect = $("#keyboardtype_select");

        // Set Application and OS
        this.selectApplication(selectedApp.name);
        selectedOS = this._getCurrentOS();

        // Init ui
        $("select.chosen-select").chosen({
            inherit_select_classes: true,
            search_contains: true
        });
        this._updateAppOptions(selectedApp.name);
        this._updateVersionOptions(selectedVersion);
        this._updateKeyboardTypeOptions(selectedKeyboardType);
        $("nav button.os-" + selectedOS).addClass("checked");
        this._initSearchBox();

        // Events
        this.elemAppSelect.on("change", function(e, parms) {
            var val = $(this).val();
            manager.selectApplication(val);
            manager._updateVersionOptions(0);
            manager._fetchAppKeydataAndUpdate();
        });
        this.elemVersionSelect.on("change", function(e, parms) {
            selectedVersion = $(this).val();
            manager._fetchAppKeydataAndUpdate();
        });
        this.elemContextSelect.on("change", function(e, parms) {
            selectedContext = $(this).val();
            manager.elemKeyboard.keyboard("option", "context", selectedContext);
        });
        $("nav button.os-radiobutton").click(function () {
            $("nav button.os-radiobutton").removeClass("checked");
            $(this).addClass("checked");
            selectedOS = $(this).attr("data-os");
            manager._fetchAppKeydataAndUpdate();
        });
        this.elemKeyboardTypeSelect.on("change", function(e, parms) {
            selectedKeyboardType = $(this).val();
            manager._updateKeyboard();
        });

        // Load in the keyboard html and available shotcut contexts
        this._fetchAppKeydataAndUpdate();
    }

    this._initSearchBox = function() {
        var manager = this;
        var results = $("#search_results");
        var input = $("#searchbox input");
        var inputBlurrer = $("#search_blurdetect");

        input.keyup(function(e) {
            manager._searchBoxUpdate(e, $(this).val());

        }).keydown(function(e) {
            // Escape key clears the search bar and hides results
            var updateHighlight = false;
            if (e.which === $.ui.keyCode.UP) {
                selectedSearchResult = Math.max(selectedSearchResult-1, 0);
                updateHighlight = true;
            } else if (e.which === $.ui.keyCode.DOWN) {
                selectedSearchResult = Math.min(selectedSearchResult+1, maxSearchResults-1);
                updateHighlight = true;
            }

            if (updateHighlight) {
                manager._searchBoxUpdate(e, $(this).val());

                if (selectedSearchResult >= 0) {
                    var s = selectedSearchShortcut;
                    manager.highlightShortcut(s.context, s.key, s.shortcut);
                }
            }

        }).focus(function(e) {
            input.addClass("active");
            //manager._searchBoxUpdate(e, $(this).val());
            inputBlurrer.show();
        });

        inputBlurrer.mousedown(function() {
            manager._exitSearch();
        });
    }

    this._appNameToHash = function(name) {
        return name.replace(" ", "")
    }

    this.selectApplication = function(name) {
        name = name.toLowerCase();
        if (name === selectedApp.name.toLowerCase())
            return;

        for (var i=0; i<sitedata_apps.length; i++) {
            if (name === sitedata_apps[i].name.toLowerCase()) {
                selectedApp = sitedata_apps[i];
                window.location.hash = "#" + this._appNameToHash(selectedApp.name);
                document.title = selectedApp.name + " Shortcuts";
                return;
            }
        }

        console.error("selected application that doesn't exist in data");
    }

    this.selectContext = function(name) {
        if (name === selectedContext)
            return;

        selectedContext = name;
        this.elemContextSelect.val(name);
        this.elemContextSelect.trigger("chosen:updated");
        this.elemKeyboard.data("keyboard").switchContext(selectedContext);
    }





    this._updateAppOptions = function(selected) {
        var applicationNames = sitedata_apps.map(function(app) { return app.name; }).sort();
        var newAppName = this._setSelectOptions(this.elemAppSelect, selected, applicationNames);

        // In case the app didn't exist in list
        if (newAppName.toLowerCase() != selected)
            this.selectApplication(newAppName);
    }

    this._updateVersionOptions = function(selected) {
        // get all versions from the keys of the selectedApp.data element
        var applicationVersions = Object.keys(selectedApp.data).sort().reverse();
        selectedVersion = this._setSelectOptions(this.elemVersionSelect, selected, applicationVersions);
    }

    this._updateContextOptions = function(selected) {
        // the datasheet contains all contexts and shortcuts for the application
        selectedContext = this._setSelectOptions(this.elemContextSelect, selected, Object.keys(selectedAppData.contexts));
    }

    this._updateKeyboardTypeOptions = function(selected) {
        selectedKeyboardType = this._setSelectOptions(this.elemKeyboardTypeSelect, selected, Object.keys(sitedata_keyboards));
    }

    this._setSelectOptions = function(element, selected, options) {
        var html_options = "";
        var max_option_length = 0;
        var final_selected = null;
        for (var i=0; i<options.length; i++) {
            var option = options[i];
            if (option.toLowerCase() === String(selected).toLowerCase() || i === selected) {
                html_options += '<option value="' + option + '" selected>' + option + '</option>';
                final_selected = option;
            } else {
                html_options += '<option value="' + option + '">' + option + '</option>';
            }
            if (option.length > max_option_length)
                max_option_length = option.length;
        }

        element.html(html_options);
        element.trigger("chosen:updated");

        if (final_selected == null)
            final_selected = options[0];

        return final_selected;
    }





    this._fetchAppKeydataAndUpdate = function(onComplete) {
        var manager = this;
        var filename = selectedApp.data[selectedVersion][selectedOS];
        $.ajax({
            url: "content/generated/" + filename,
            dataType: "json"
        }).done(function (keydata) {
            selectedAppData = keydata;
            selectedContext = keydata.default_context;
            manager._updateContextOptions(selectedContext);
            manager._updateKeyboard();
        }).fail(function() {
            $("#keycontent").html("There is no data available for this OS or App Version (try selecting a different app version)");
        });
    }

    this._updateKeyboard = function() {
        // Clear keyboard html contents
        // Todo: add some sort of loading thing
        $("#keycontent").html("");

        var manager = this;
        var filename = sitedata_keyboards[selectedKeyboardType][selectedOS];
        $.ajax({
            url: "content/keyboards/" + filename,
            dataType: "html"
        }).done(function (content) {

            // Strip stylesheet from content and add to page DOM
            content = content.replace(/<link\b[^>]*>/i,"")
            $("#keycontent").html(content);

            // Init the keyboard widget
            manager.elemKeyboard = $("#keyboard");
            manager.elemKeyboard.keyboard({
                'keydata': selectedAppData.contexts,
                'mods': selectedAppData.mods_used,
                'context': selectedContext
            });
            manager.elemKeyboard.show();
        }).fail(function() {
            $("#keycontent").html("KEYBOARD NOT FOUND (Possibly doesn't exist for selected OS)");
        });
    }

    this._getCurrentOS = function() {
        var appver = navigator.appVersion.toLowerCase();
        if (appver.indexOf("win")!=-1)
            return "windows";
        if (appver.indexOf("mac")!=-1)
            return "mac";
        if (appver.indexOf("linux")!=-1)
            return "linux";
        return "windows";
    }








    this._exitSearch = function() {
        $("#searchbox input").removeClass("active");
        selectedSearchResult = -1;
        $("#search_results").hide();
        $("#search_blurdetect").hide();
        this.elemKeyboard.data("keyboard").exitHighlightMode();
    }

    this._searchBoxUpdate = function(e, searchText) {
        var input = $("#searchbox input");
        var results = $("#search_results");

        // Escape key clears the search bar and hides results
        if (e.which === $.ui.keyCode.ESCAPE) {
            input.val("").blur();
            this._exitSearch();
            e.stopImmediatePropagation();
            return;
        }

        // Only search past centrain length
        if (searchText.length < minSearchLength) {
            selectedSearchResult = -1;
            results.hide();
            return;
        }

        var escapedSearchText = searchText.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
        var regex = new RegExp(escapedSearchText, 'i');
        var zregex = new RegExp(escapedSearchText, 'i');

        // Iterate through our shortcuts data and build a table for results
        var html = "<table><tbody>";
        var numResults = 0;
        var numContexts = Object.keys(selectedAppData.contexts).length;
        for (var contextName in selectedAppData.contexts) {
            var context = selectedAppData.contexts[contextName];

            for (var keyName in context) {

                var shortcuts = context[keyName];
                for (i=0; i<shortcuts.length; i++) {
                    var shortcut = shortcuts[i];
                    var name = shortcut.name;
                    if (regex.test(name)) {

                        // Don't show more than max
                        if (numResults >= maxSearchResults) {
                            numResults++;
                            continue;
                        }

                        // Keep track of selected result
                        if (selectedSearchResult === numResults) {
                            selectedSearchShortcut.context = contextName;
                            selectedSearchShortcut.key = keyName;
                            selectedSearchShortcut.shortcut = shortcut;
                        }

                        html += (selectedSearchResult === numResults) ? "<tr class='selected'>" : "<tr>";

                        // Keys
                        html += "<td>";
                        for (m=0; m<shortcut.mods.length; m++) {
                            var mod = shortcut.mods[m].toLowerCase();
                            html += "<span class='" + mod + "'>" + mod + "</span>";
                        }
                        html += "<span>" + keyName + "</span></td>";

                        // Shortcut Name
                        html += "<td>";
                        var pos = name.search(zregex);
                        html += name.substring(0, pos) + "<em>" + name.substring(pos, pos + searchText.length) + "</em>" + name.substring(pos + searchText.length);
                        html += "</td>";

                        // Context (only if there are multiple)
                        if (numContexts > 1)
                            html += "<td>" + contextName + "</td>";

                        html += "</tr>";

                        numResults++;
                    }
                }
            }
        }
        html += "</tbody></table>";

        // Makes sure the user knows there are more
        if ((numResults-maxSearchResults) > 0) {
            html += "<span class='more-results'>" + (numResults-maxSearchResults) + " more shortcuts found...</span>";
        }

        // Show results and center content
        if (numResults > 0) {
            results.html(html);
            results.css("left", input.outerWidth()/2 - results.width()/2);
            results.show();
        } else if (numResults == 0) {
            selectedSearchResult = -1;
            results.hide();
        }
    }

    this.highlightShortcut = function(contextName, keyName, shortcut) {
        this.selectContext(contextName);
        this.elemKeyboard.data("keyboard").highlightShortcut(keyName, shortcut);
    }
}

var pageManager = new function PageManager() {

    selectedApp = sitedata_apps[0];
    selectedAppKeyData = null;
    selectedVersion = null;
    selectedContext = null;
    selectedOS = null;
    selectedKeyboardType = null;

    this.init = function() {
        var manager = this;

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

        // Events
        this.elemAppSelect.on("change", function(e, parms) {
            var val = $(this).val();
            console.log("elemAppSelect changed to " + val);

            manager.selectApplication(val);
            manager._updateVersionOptions(0);

            manager._fetchAppKeydata(function() {
                manager._updateContextOptions(selectedContext);
                manager._updateKeyboard();
            });
        });
        this.elemVersionSelect.on("change", function(e, parms) {
            console.log("elemVersionSelect changed to " + $(this).val());

            selectedVersion = $(this).val();

            manager._fetchAppKeydata(function() {
                manager._updateContextOptions(selectedContext);
                manager._updateKeyboard();
            });
        });
        this.elemContextSelect.on("change", function(e, parms) {
            console.log("elemContextSelect changed to " + $(this).val());

            selectedContext = $(this).val();
            manager.elemKeyboard.keyboard("option", "context", selectedContext);
        });
        $("nav button.os-radiobutton").click(function () {
            $("nav button.os-radiobutton").removeClass("checked");
            $(this).addClass("checked");
            selectedOS = $(this).attr("data-os");

            manager._fetchAppKeydata(function() {
                manager._updateContextOptions(selectedContext);
                manager._updateKeyboard();
            });
        });
        this.elemKeyboardTypeSelect.on("change", function(e, parms) {
            console.log("elemKeyboardTypeSelect changed to " + $(this).val());

            selectedKeyboardType = $(this).val();
            manager._updateKeyboard();
        });

        // Load in the keyboard html and available shotcut contexts
        this._fetchAppKeydata(function() {
            manager._updateContextOptions(selectedContext);
            manager._updateKeyboard();
        });
    }


    this.selectApplication = function(name) {
        name = name.toLowerCase();
        if (name === selectedApp.name.toLowerCase())
            return;

        for (var i=0; i<sitedata_apps.length; i++) {
            if (name === sitedata_apps[i].name.toLowerCase()) {
                selectedApp = sitedata_apps[i];
                window.location.hash = "#" + selectedApp.name;
                document.title = selectedApp.name + " Shortcuts";
                return;
            }
        }

        console.error("selected application that doesn't exist in data");
    }





    this._updateAppOptions = function(selected) {
        var applicationNames = sitedata_apps.map(function(app) { return app.name; }).sort();
        var newAppName = this.set_select_options(this.elemAppSelect, selected, applicationNames);

        // In case the app didn't exist in list
        if (newAppName.toLowerCase() != selected)
            this.selectApplication(newAppName);
    }

    this._updateVersionOptions = function(selected) {
        // get all versions from the keys of the selectedApp.data element
        selectedVersion = this.set_select_options(this.elemVersionSelect, selected, Object.keys(selectedApp.data));
    }

    this._updateContextOptions = function(selected) {
        // the datasheet contains all contexts and shortcuts for the application
        selectedContext = this.set_select_options(this.elemContextSelect, selected, Object.keys(selectedAppKeyData.contexts));
    }

    this._updateKeyboardTypeOptions = function(selected) {
        selectedKeyboardType = this.set_select_options(this.elemKeyboardTypeSelect, selected, Object.keys(sitedata_keyboards));
    }


    this._fetchAppKeydata = function(onComplete) {
        var filename = selectedApp.data[selectedVersion][selectedOS];
        console.log("update_app_keydata: " + filename);

        $.ajax({
            url: "appdata/" + filename,
            dataType: "json"
        }).done(function (keydata) {
            console.log("loaded app key data: " + filename);

            selectedAppKeyData = keydata;
            onComplete();
        }).fail(function() {
            $("#keycontent").html("There is no export available for this OS");
        });
    }

    this._updateKeyboard = function() {
        // Clear keyboard html contents
        // Todo: add some sort of loading thing
        $("#keycontent").html("");

        var manager = this;
        var filename = sitedata_keyboards[selectedKeyboardType][selectedOS];
        $.ajax({
            url: "keyboards/" + filename,
            dataType: "html"
        }).done(function (content) {

            // Strip stylesheet from content and add to page DOM
            content = content.replace(/<link\b[^>]*>/i,"")
            $("#keycontent").html(content);

            // Init the keyboard widget
            manager.elemKeyboard = $("#keyboard");
            manager.elemKeyboard.keyboard({
                'keydata': selectedAppKeyData.contexts,
                'mods': selectedAppKeyData.mods_used,
                'context': selectedContext
            });
            manager.elemKeyboard.show();
        }).fail(function() {
            $("#keycontent").html("KEYBOARD NOT FOUND");
        });
    }


    this.set_select_options = function(element, selected, options) {
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
        element.chosen("option", "disable_search", options.length <= 5);
        element.trigger("chosen:updated");

        if (final_selected == null)
            final_selected = options[0];

        return final_selected;
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
}

"use strict";
var page = require('webpage').create(),
    system = require('system'),
    address, output, size;
function onPageReady() {
    var htmlContent = page.evaluate(function () {
        return document.documentElement.outerHTML;
    });

    console.log(htmlContent);

    phantom.exit();
}

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: rasterize.js URL filename');
    console.log('  image size: 1301*8000');
    console.log('  image (png/jpg output) examples: "1920px" entire page, window width 1920px');
    
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 1920*22, height: 1000 };
    if (system.args.length > 3 && system.args[2].substr(-4) === ".pdf") {
        size = system.args[3].split('*');
        page.paperSize = size.length === 2 ? { width: size[0], height: size[1], margin: '0px' }
                                           : { format: system.args[3], orientation: 'portrait', margin: '1cm' };
    } else if (system.args.length > 3 && system.args[3].substr(-2) === "px") {
        size = system.args[3].split('*');
        if (size.length === 2) {
            pageWidth = parseInt(size[0], 10);
            pageHeight = parseInt(size[1], 10);
            page.viewportSize = { width: pageWidth, height: pageHeight };
            page.clipRect = { top: 0, left: 0, width: pageWidth, height: pageHeight };
        } else {
            console.log("size:", system.args[3]);
            pageWidth = parseInt(system.args[3], 10);
            pageHeight = parseInt(pageWidth * 10, 10); // it's as good an assumption as any
            console.log ("pageHeight:",pageHeight);
            page.viewportSize = { width: pageWidth, height: pageHeight };
        }
    }
    if (system.args.length > 4) {
        page.zoomFactor = system.args[4];
    }
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit(1);
        } else {
            window.setTimeout(function () {
                page.render(output);
                console.log('   image saved:', output);
                phantom.exit();
            }, 200);

        }
    });
//    page.open(address, function (status) {
//        function checkReadyState() {
//            setTimeout(function () {
//                var readyState = page.evaluate(function () {
//                    return document.readyState;
//            });
//
//            if ("complete" === readyState) {
//                //onPageReady();
//                page.render(output);
//                console.log(" image saved");
//            } else {
//                checkReadyState();
//            }
//        });
//        }

//        checkReadyState();
//    });
}

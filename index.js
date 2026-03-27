/**
 * Lottie Dynamic Bridge
 * Fix: Added safety checks (Null checks) for currentData to prevent crashes.
 */

window.animLoaded = false;
window.anim = null;

window.initLottie = function(jsonData) {
    document.fonts.ready.then(() => {
        window.anim = lottie.loadAnimation({
            container: document.getElementById('bm'),
            renderer: 'svg',
            loop: false,
            autoplay: false,
            animationData: jsonData,
            rendererSettings: {
                preserveAspectRatio: 'xMidYMid slice' 
            }
        });

        window.anim.addEventListener('DOMLoaded', () => { 
            window.animLoaded = true; 
        });
    });
};

window.updateLayerText = function(layerName, newText) {
    if (!window.anim || !newText) return;

    const findAndModify = (elements) => {
        elements.forEach(el => {
            if (el.data && el.data.nm === layerName && el.updateDocumentData) {
                
                // SAFETY CHECK: Ensure currentData exists before reading 'f'
                let fontToPreserve = null;
                if (el.currentData && el.currentData.f) {
                    fontToPreserve = el.currentData.f;
                }
                
                // Prepare update object
                const updateParams = { t: String(newText) };
                
                // If we found a font, add it to parameters to preserve weight
                if (fontToPreserve) {
                    updateParams.f = fontToPreserve;
                }

                el.updateDocumentData(updateParams, 0);
            }
            if (el.elements) findAndModify(el.elements);
        });
    };

    findAndModify(window.anim.renderer.elements);
};
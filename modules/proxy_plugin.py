import json
import os

def proxy_plugin(proxy):
    proxy= proxy.split(':')
    PROXY_HOST = proxy[0]
    PROXY_PORT = proxy[1]
    PROXY_USER = proxy[2]
    PROXY_PASS = proxy[3]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfolder = 'proxy_auth_plugin'
    
    if not os.path.exists(pluginfolder):
            os.mkdir(pluginfolder)

    with open(f'{pluginfolder}/manifest.json', 'w', encoding='utf-8') as f:
        f.write(manifest_json)
        
    with open(f'{pluginfolder}/background.js', 'w', encoding='utf-8') as f:
        f.write(background_js)
    
    return pluginfolder
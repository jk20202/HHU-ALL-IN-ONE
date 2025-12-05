const crypto = require('crypto');

function generateFingerPrint() {
    // MD5 哈希函数
    function md5(data) {
        const hash = crypto.createHash('md5');
        if (Array.isArray(data)) {
            const buffer = Buffer.from(data);
            hash.update(buffer);
        } else {
            hash.update(data.toString());
        }
        return hash.digest('hex').toUpperCase();
    }

    // 模拟 Canvas 数据
    function createDataUrl() {
        const txt = "WiseduCiap,com <canvas> 1.0";
        const mockCanvasData = txt + "_mock_canvas_data";
        return {
            dataUrl: "data:image/png;base64," + Buffer.from(mockCanvasData).toString('base64'),
            rawData: mockCanvasData
        };
    }

    // 生成 Canvas Hash
    function createHash(rawData) {
        if (!rawData) return "N/A";
        const dataArr = [];
        for (let i = 0; i < rawData.length; i++) {
            dataArr.push(rawData.charCodeAt(i));
        }
        return md5(dataArr);
    }

    // 固定的浏览器信息
    const browserInfo = {
        browser: "Chrome",
        engine: "Blink",
        os: "Windows",
        cpu: "amd64",
        deviceType: "-",
        deviceModel: "-",
        deviceVendor: "-"
    };

    // 固定的 Navigator 信息
    const navigatorInfo = {
        platform: "Win32",
        language: "zh-CN",
        hardwareConcurrency: 8,
        maxTouchPoints: 0,
        deviceMemory: 8
    };

    // 生成 canvas 指纹
    const canvasData = createDataUrl();
    const canvasHash = createHash(canvasData.rawData);

    // 生成混合 hash
    const items = [
        browserInfo.browser,
        browserInfo.engine,
        browserInfo.os,
        browserInfo.cpu,
        browserInfo.deviceType,
        browserInfo.deviceModel,
        browserInfo.deviceVendor,
        navigatorInfo.platform,
        navigatorInfo.language,
        navigatorInfo.hardwareConcurrency.toString(),
        navigatorInfo.maxTouchPoints.toString(),
        navigatorInfo.deviceMemory.toString(),
        canvasHash
    ];

    return md5(items.join("|"));

}

// 使用示例
// const fingerprint = generateFingerPrint();
// console.log('Generated fingerprint:', fingerprint);


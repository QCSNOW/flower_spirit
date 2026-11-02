using System;
using System.Drawing;
using System.Drawing.Imaging;

class GenTex2 {
    static void Main() {
        // 1. 繁花结晶 - 棱晶结构，小尺寸，紫粉蓝渐变
        MakeCrystal(@"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_crystal.png");
        Console.WriteLine("OK: flower_crystal.png");

        // 2. 繁花之戒 - 铁银色，居中
        MakeRing(@"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_spirit_ring.png");
        Console.WriteLine("OK: flower_spirit_ring.png");

        // 3. 繁花吊坠 - 铁银色，居中
        MakeAmulet(@"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_spirit_amulet.png");
        Console.WriteLine("OK: flower_spirit_amulet.png");
    }

    // 繁花结晶：菱形多面棱晶，约占 10x12 像素，紫-粉-青渐变
    static void MakeCrystal(string path) {
        using(Bitmap bmp = new Bitmap(16, 16, PixelFormat.Format32bppArgb)) {
            // 配色
            Color c_darkPurple = Color.FromArgb(255, 80, 30, 120);    // 深紫（轮廓阴影）
            Color c_purple = Color.FromArgb(255, 140, 60, 180);       // 紫色
            Color c_pink = Color.FromArgb(255, 220, 110, 200);        // 粉色
            Color c_lightPink = Color.FromArgb(255, 255, 170, 230);   // 亮粉
            Color c_cyan = Color.FromArgb(255, 120, 220, 255);        // 青色核心
            Color c_white = Color.FromArgb(255, 240, 240, 255);       // 高光白

            // 结晶形状：菱形，10x12，居中
            // 行从 y=2 到 y=13（12行高）
            // 列中心 x=7.5，宽度逐行变化

            // y=2: 1像素宽 (x=7)
            SetPx(bmp, 7, 2, c_white);
            // y=3: 3像素宽 (x=6-8)
            SetPx(bmp, 6, 3, c_lightPink); SetPx(bmp, 7, 3, c_white); SetPx(bmp, 8, 3, c_lightPink);
            // y=4: 5像素宽 (x=5-9)
            SetPx(bmp, 5, 4, c_pink); SetPx(bmp, 6, 4, c_lightPink); SetPx(bmp, 7, 4, c_white); SetPx(bmp, 8, 4, c_lightPink); SetPx(bmp, 9, 4, c_pink);
            // y=5: 7像素宽 (x=4-10)
            SetPx(bmp, 4, 5, c_purple); SetPx(bmp, 5, 5, c_pink); SetPx(bmp, 6, 5, c_lightPink); SetPx(bmp, 7, 5, c_cyan); SetPx(bmp, 8, 5, c_lightPink); SetPx(bmp, 9, 5, c_pink); SetPx(bmp, 10, 5, c_purple);
            // y=6: 9像素宽 (x=3-11) - 最宽处
            SetPx(bmp, 3, 6, c_darkPurple); SetPx(bmp, 4, 6, c_purple); SetPx(bmp, 5, 6, c_pink); SetPx(bmp, 6, 6, c_lightPink); SetPx(bmp, 7, 6, c_cyan); SetPx(bmp, 8, 6, c_lightPink); SetPx(bmp, 9, 6, c_pink); SetPx(bmp, 10, 6, c_purple); SetPx(bmp, 11, 6, c_darkPurple);
            // y=7: 9像素宽 - 中层（棱面阴影）
            SetPx(bmp, 3, 7, c_darkPurple); SetPx(bmp, 4, 7, c_purple); SetPx(bmp, 5, 7, c_pink); SetPx(bmp, 6, 7, c_pink); SetPx(bmp, 7, 7, c_lightPink); SetPx(bmp, 8, 7, c_pink); SetPx(bmp, 9, 7, c_pink); SetPx(bmp, 10, 7, c_purple); SetPx(bmp, 11, 7, c_darkPurple);
            // y=8: 7像素宽
            SetPx(bmp, 4, 8, c_darkPurple); SetPx(bmp, 5, 8, c_purple); SetPx(bmp, 6, 8, c_pink); SetPx(bmp, 7, 8, c_pink); SetPx(bmp, 8, 8, c_pink); SetPx(bmp, 9, 8, c_purple); SetPx(bmp, 10, 8, c_darkPurple);
            // y=9: 7像素宽（下半部分，更暗）
            SetPx(bmp, 4, 9, c_darkPurple); SetPx(bmp, 5, 9, c_purple); SetPx(bmp, 6, 9, c_purple); SetPx(bmp, 7, 9, c_pink); SetPx(bmp, 8, 9, c_purple); SetPx(bmp, 9, 9, c_purple); SetPx(bmp, 10, 9, c_darkPurple);
            // y=10: 5像素宽
            SetPx(bmp, 5, 10, c_darkPurple); SetPx(bmp, 6, 10, c_purple); SetPx(bmp, 7, 10, c_pink); SetPx(bmp, 8, 10, c_purple); SetPx(bmp, 9, 10, c_darkPurple);
            // y=11: 3像素宽
            SetPx(bmp, 6, 11, c_darkPurple); SetPx(bmp, 7, 11, c_purple); SetPx(bmp, 8, 11, c_darkPurple);
            // y=12: 1像素宽
            SetPx(bmp, 7, 12, c_darkPurple);

            // 棱晶切面高光（对角线亮线，表现多面体结构）
            SetPx(bmp, 6, 5, c_white);  // 左侧高光点
            SetPx(bmp, 5, 6, c_lightPink);
            SetPx(bmp, 9, 7, c_lightPink); // 右侧棱线

            bmp.Save(path, ImageFormat.Png);
        }
    }

    // 繁花之戒：铁银色指环 + 粉色宝石，居中
    static void MakeRing(string path) {
        using(Bitmap bmp = new Bitmap(16, 16, PixelFormat.Format32bppArgb)) {
            // 铁银色
            Color ironDark = Color.FromArgb(255, 100, 100, 110);
            Color iron = Color.FromArgb(255, 160, 160, 175);
            Color ironLight = Color.FromArgb(255, 210, 210, 220);
            Color ironHighlight = Color.FromArgb(255, 240, 240, 245);

            // 宝石
            Color gemDark = Color.FromArgb(255, 170, 60, 120);
            Color gem = Color.FromArgb(255, 220, 100, 170);
            Color gemLight = Color.FromArgb(255, 255, 150, 200);
            Color gemHighlight = Color.FromArgb(255, 255, 220, 240);

            // 戒指：指环外径约 10 像素，内径约 6 像素
            // 顶部弧
            SetPx(bmp, 5, 3, ironDark); SetPx(bmp, 6, 2, iron); SetPx(bmp, 7, 2, ironLight); SetPx(bmp, 8, 2, iron); SetPx(bmp, 9, 3, ironDark);
            SetPx(bmp, 4, 4, ironDark); SetPx(bmp, 5, 4, ironLight); SetPx(bmp, 6, 3, ironLight); SetPx(bmp, 7, 3, ironHighlight); SetPx(bmp, 8, 3, ironLight); SetPx(bmp, 9, 4, iron); SetPx(bmp, 10, 4, ironDark);
            // 左右两侧
            SetPx(bmp, 3, 5, ironDark); SetPx(bmp, 3, 6, iron); SetPx(bmp, 3, 7, iron); SetPx(bmp, 3, 8, ironDark);
            SetPx(bmp, 12, 5, ironDark); SetPx(bmp, 12, 6, iron); SetPx(bmp, 12, 7, iron); SetPx(bmp, 12, 8, ironDark);
            SetPx(bmp, 4, 5, ironLight); SetPx(bmp, 4, 6, ironLight); SetPx(bmp, 4, 7, ironLight); SetPx(bmp, 4, 8, iron);
            SetPx(bmp, 11, 5, ironLight); SetPx(bmp, 11, 6, ironLight); SetPx(bmp, 11, 7, ironLight); SetPx(bmp, 11, 8, iron);
            // 底部弧
            SetPx(bmp, 5, 9, ironDark); SetPx(bmp, 6, 10, ironDark); SetPx(bmp, 7, 10, ironDark); SetPx(bmp, 8, 10, ironDark); SetPx(bmp, 9, 9, ironDark);
            SetPx(bmp, 5, 8, iron); SetPx(bmp, 6, 9, iron); SetPx(bmp, 7, 9, iron); SetPx(bmp, 8, 9, iron); SetPx(bmp, 9, 8, iron);
            SetPx(bmp, 6, 8, ironLight); SetPx(bmp, 7, 8, ironLight); SetPx(bmp, 8, 8, ironLight);

            // 中间粉色宝石（4x5，居中）
            SetPx(bmp, 7, 4, gemHighlight);
            SetPx(bmp, 6, 5, gemLight); SetPx(bmp, 7, 5, gemHighlight); SetPx(bmp, 8, 5, gemLight);
            SetPx(bmp, 6, 6, gem); SetPx(bmp, 7, 6, gemLight); SetPx(bmp, 8, 6, gem);
            SetPx(bmp, 6, 7, gemDark); SetPx(bmp, 7, 7, gem); SetPx(bmp, 8, 7, gemDark);

            bmp.Save(path, ImageFormat.Png);
        }
    }

    // 繁花吊坠：铁银色链条 + 悬挂的繁花结晶，居中
    static void MakeAmulet(string path) {
        using(Bitmap bmp = new Bitmap(16, 16, PixelFormat.Format32bppArgb)) {
            Color ironDark = Color.FromArgb(255, 100, 100, 110);
            Color iron = Color.FromArgb(255, 160, 160, 175);
            Color ironLight = Color.FromArgb(255, 210, 210, 220);

            Color crystalDark = Color.FromArgb(255, 100, 40, 140);
            Color crystal = Color.FromArgb(255, 180, 80, 200);
            Color crystalLight = Color.FromArgb(255, 255, 150, 230);
            Color crystalHighlight = Color.FromArgb(255, 255, 220, 250);

            // 链条（顶部 V 形，居中）
            // 左侧链
            SetPx(bmp, 4, 1, ironDark); SetPx(bmp, 5, 2, iron); SetPx(bmp, 6, 3, ironLight);
            // 右侧链
            SetPx(bmp, 11, 1, ironDark); SetPx(bmp, 10, 2, iron); SetPx(bmp, 9, 3, ironLight);
            // 顶部横杆
            SetPx(bmp, 7, 4, ironDark); SetPx(bmp, 8, 4, ironDark);
            SetPx(bmp, 7, 3, iron); SetPx(bmp, 8, 3, iron);
            SetPx(bmp, 6, 4, ironLight); SetPx(bmp, 9, 4, ironLight);

            // 挂扣
            SetPx(bmp, 7, 5, ironDark); SetPx(bmp, 8, 5, ironDark);
            SetPx(bmp, 7, 6, iron); SetPx(bmp, 8, 6, iron);

            // 繁花结晶（吊坠主体，菱形，约 8x7，居中偏下）
            // y=7: 顶端 1像素
            SetPx(bmp, 7, 7, crystalHighlight);
            // y=8: 3像素
            SetPx(bmp, 6, 8, crystalLight); SetPx(bmp, 7, 8, crystalHighlight); SetPx(bmp, 8, 8, crystalLight);
            // y=9: 5像素 - 最宽
            SetPx(bmp, 5, 9, crystal); SetPx(bmp, 6, 9, crystalLight); SetPx(bmp, 7, 9, crystalHighlight); SetPx(bmp, 8, 9, crystalLight); SetPx(bmp, 9, 9, crystal);
            // y=10: 5像素（下棱面）
            SetPx(bmp, 5, 10, crystalDark); SetPx(bmp, 6, 10, crystal); SetPx(bmp, 7, 10, crystalLight); SetPx(bmp, 8, 10, crystal); SetPx(bmp, 9, 10, crystalDark);
            // y=11: 3像素
            SetPx(bmp, 6, 11, crystalDark); SetPx(bmp, 7, 11, crystal); SetPx(bmp, 8, 11, crystalDark);
            // y=12: 1像素底端
            SetPx(bmp, 7, 12, crystalDark);

            // 结晶上的小花点缀
            SetPx(bmp, 6, 9, Color.FromArgb(255, 255, 100, 180));
            SetPx(bmp, 8, 9, Color.FromArgb(255, 255, 100, 180));

            bmp.Save(path, ImageFormat.Png);
        }
    }

    static void SetPx(Bitmap bmp, int x, int y, Color c) {
        if(x >= 0 && x < bmp.Width && y >= 0 && y < bmp.Height) {
            bmp.SetPixel(x, y, c);
        }
    }
}

using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;

class GenTex {
    static void Main() {
        // 1. 繁花结晶
        MakeCrystal(
            @"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_crystal_gen.jpg",
            @"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_crystal.png",
            16, 16
        );
        Console.WriteLine("OK: flower_crystal.png");

        // 2. 繁花之戒（戒指形状，粉金配色，镶嵌小结晶）
        MakeRing(
            @"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_spirit_ring.png",
            16, 16
        );
        Console.WriteLine("OK: flower_spirit_ring.png");

        // 3. 繁花吊坠（项链形状，吊着结晶）
        MakeAmulet(
            @"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_spirit_amulet.png",
            16, 16
        );
        Console.WriteLine("OK: flower_spirit_amulet.png");
    }

    static void MakeCrystal(string srcPath, string dstPath, int w, int h) {
        using(Bitmap src = new Bitmap(srcPath)) {
            int cx = src.Width / 2;
            int cy = src.Height / 2;
            int sz = (int)(src.Width * 0.55);
            Rectangle r = new Rectangle(cx - sz/2, cy - sz/2, sz, sz);
            using(Bitmap crop = src.Clone(r, src.PixelFormat))
            using(Bitmap dst = new Bitmap(w, h, PixelFormat.Format32bppArgb)) {
                using(Graphics g = Graphics.FromImage(dst)) {
                    g.InterpolationMode = InterpolationMode.NearestNeighbor;
                    g.PixelOffsetMode = PixelOffsetMode.Half;
                    g.DrawImage(crop, 0, 0, w, h);
                }
                // 白色/近白变透明
                for(int y = 0; y < h; y++)
                for(int x = 0; x < w; x++) {
                    Color c = dst.GetPixel(x, y);
                    if(c.R > 220 && c.G > 220 && c.B > 220) {
                        dst.SetPixel(x, y, Color.FromArgb(0, c.R, c.G, c.B));
                    }
                }
                dst.Save(dstPath, ImageFormat.Png);
            }
        }
    }

    // 戒指：金色指环 + 中间粉色宝石
    static void MakeRing(string path, int w, int h) {
        using(Bitmap bmp = new Bitmap(w, h, PixelFormat.Format32bppArgb)) {
            // 戒指轮廓（像素画风格，16x16）
            // 指环部分：金色
            Color goldLight = Color.FromArgb(255, 255, 215, 100);
            Color gold = Color.FromArgb(255, 218, 165, 32);
            Color goldDark = Color.FromArgb(255, 184, 134, 11);

            // 中间宝石
            Color gemLight = Color.FromArgb(255, 255, 150, 200);
            Color gem = Color.FromArgb(255, 220, 100, 170);
            Color gemDark = Color.FromArgb(255, 170, 60, 120);

            // 画戒指环
            // 顶部弧线
            SetPx(bmp, 5, 2, goldDark); SetPx(bmp, 6, 1, gold); SetPx(bmp, 7, 1, gold); SetPx(bmp, 8, 1, gold); SetPx(bmp, 9, 2, goldDark);
            SetPx(bmp, 4, 3, goldDark); SetPx(bmp, 5, 3, goldLight); SetPx(bmp, 6, 2, goldLight); SetPx(bmp, 7, 2, goldLight); SetPx(bmp, 8, 2, goldLight); SetPx(bmp, 9, 3, gold); SetPx(bmp, 10, 3, goldDark);
            // 左右两侧
            SetPx(bmp, 3, 4, goldDark); SetPx(bmp, 3, 5, gold); SetPx(bmp, 3, 6, gold); SetPx(bmp, 3, 7, goldDark);
            SetPx(bmp, 12, 4, goldDark); SetPx(bmp, 12, 5, gold); SetPx(bmp, 12, 6, gold); SetPx(bmp, 12, 7, goldDark);
            SetPx(bmp, 4, 4, goldLight); SetPx(bmp, 4, 5, goldLight); SetPx(bmp, 4, 6, goldLight); SetPx(bmp, 4, 7, gold);
            SetPx(bmp, 11, 4, goldLight); SetPx(bmp, 11, 5, goldLight); SetPx(bmp, 11, 6, goldLight); SetPx(bmp, 11, 7, gold);
            // 底部弧线
            SetPx(bmp, 5, 8, goldDark); SetPx(bmp, 6, 9, goldDark); SetPx(bmp, 7, 9, goldDark); SetPx(bmp, 8, 9, goldDark); SetPx(bmp, 9, 8, goldDark);
            SetPx(bmp, 5, 7, gold); SetPx(bmp, 6, 8, gold); SetPx(bmp, 7, 8, gold); SetPx(bmp, 8, 8, gold); SetPx(bmp, 9, 7, gold);
            SetPx(bmp, 6, 7, goldLight); SetPx(bmp, 7, 7, goldLight); SetPx(bmp, 8, 7, goldLight);

            // 中间宝石（粉色菱形，4x5）
            SetPx(bmp, 7, 3, gemLight);
            SetPx(bmp, 6, 4, gem); SetPx(bmp, 7, 4, gemLight); SetPx(bmp, 8, 4, gem);
            SetPx(bmp, 6, 5, gemDark); SetPx(bmp, 7, 5, gem); SetPx(bmp, 8, 5, gemDark);
            SetPx(bmp, 7, 6, gemDark);

            bmp.Save(path, ImageFormat.Png);
        }
    }

    // 吊坠：金项链 + 悬挂的繁花结晶
    static void MakeAmulet(string path, int w, int h) {
        using(Bitmap bmp = new Bitmap(w, h, PixelFormat.Format32bppArgb)) {
            Color goldLight = Color.FromArgb(255, 255, 215, 100);
            Color gold = Color.FromArgb(255, 218, 165, 32);
            Color goldDark = Color.FromArgb(255, 184, 134, 11);

            Color crystalLight = Color.FromArgb(255, 255, 200, 255);
            Color crystal = Color.FromArgb(255, 220, 140, 220);
            Color crystalDark = Color.FromArgb(255, 170, 80, 170);

            // 项链链条（顶部 U 形）
            SetPx(bmp, 3, 0, goldDark); SetPx(bmp, 4, 1, gold); SetPx(bmp, 5, 2, gold);
            SetPx(bmp, 12, 0, goldDark); SetPx(bmp, 11, 1, gold); SetPx(bmp, 10, 2, gold);
            SetPx(bmp, 6, 3, gold); SetPx(bmp, 7, 3, goldLight); SetPx(bmp, 8, 3, gold); SetPx(bmp, 9, 3, gold);

            // 链条细节
            SetPx(bmp, 3, 1, gold); SetPx(bmp, 12, 1, gold);
            SetPx(bmp, 4, 2, goldLight); SetPx(bmp, 11, 2, goldLight);
            SetPx(bmp, 5, 3, goldLight); SetPx(bmp, 10, 3, goldLight);

            // 吊坠顶部的挂扣
            SetPx(bmp, 7, 4, goldDark); SetPx(bmp, 8, 4, goldDark);
            SetPx(bmp, 7, 5, gold); SetPx(bmp, 8, 5, gold);

            // 繁花结晶（吊坠主体，钻石形状，8x7）
            // 顶部尖
            SetPx(bmp, 7, 6, crystalLight);
            // 第二层
            SetPx(bmp, 6, 7, crystal); SetPx(bmp, 7, 7, crystalLight); SetPx(bmp, 8, 7, crystal);
            // 中间层（最宽）
            SetPx(bmp, 5, 8, crystalDark); SetPx(bmp, 6, 8, crystal); SetPx(bmp, 7, 8, crystalLight); SetPx(bmp, 8, 8, crystal); SetPx(bmp, 9, 8, crystalDark);
            // 第四层
            SetPx(bmp, 6, 9, crystalDark); SetPx(bmp, 7, 9, crystal); SetPx(bmp, 8, 9, crystalDark);
            // 底部尖
            SetPx(bmp, 7, 10, crystalDark);

            // 结晶上的小花点缀（2个小粉点）
            SetPx(bmp, 6, 8, Color.FromArgb(255, 255, 100, 180));
            SetPx(bmp, 8, 8, Color.FromArgb(255, 255, 100, 180));

            bmp.Save(path, ImageFormat.Png);
        }
    }

    static void SetPx(Bitmap bmp, int x, int y, Color c) {
        if(x >= 0 && x < bmp.Width && y >= 0 && y < bmp.Height) {
            bmp.SetPixel(x, y, c);
        }
    }
}

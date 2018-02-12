using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_00_WPF
{
    public partial class OptionForm : Form
    {
        public OptionForm()
        {
            InitializeComponent();
        }

        #region 初期処理
        private void OptionForm_Load(object sender, EventArgs e)
        {
            //初期化処理
            //// マウス移動イベントを追加
            this.MouseDown += new MouseEventHandler(Form_MouseDown);
            this.MouseMove += new MouseEventHandler(Form_MouseMove);

            //エンターキーを割り当てる
            this.AcceptButton = this.ApplyButton;

        }
        #endregion

        #region フォーム操作
        // マウスポインタの位置を保存する
        private Point mousePoint;

        //マウスのボタンが押されたとき
        private void Form_MouseDown(object sender, MouseEventArgs e)
        {
            if ((e.Button & MouseButtons.Left) == MouseButtons.Left)
            {
                //位置を記憶する
                mousePoint = new Point(e.X, e.Y);
            }
        }

        //マウスが動いたとき
        private void Form_MouseMove(object sender, MouseEventArgs e)
        {
            if ((e.Button & MouseButtons.Left) == MouseButtons.Left)
            {
                this.Left += e.X - mousePoint.X;
                this.Top += e.Y - mousePoint.Y;
            }
        }
        #endregion

       
    }
}

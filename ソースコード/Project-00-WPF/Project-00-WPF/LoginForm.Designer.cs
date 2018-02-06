namespace Project_00_WPF
{
    partial class LoginForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.CloseButton = new System.Windows.Forms.Button();
            this.LoginIdLavel = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.LoginPasswordText = new System.Windows.Forms.TextBox();
            this.LoginIdText = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.LoginButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // CloseButton
            // 
            this.CloseButton.BackColor = System.Drawing.Color.PaleVioletRed;
            this.CloseButton.FlatAppearance.BorderSize = 0;
            this.CloseButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.CloseButton.Font = new System.Drawing.Font("メイリオ", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.CloseButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.CloseButton.Location = new System.Drawing.Point(319, -1);
            this.CloseButton.Name = "CloseButton";
            this.CloseButton.Size = new System.Drawing.Size(40, 34);
            this.CloseButton.TabIndex = 4;
            this.CloseButton.Text = "✖";
            this.CloseButton.UseVisualStyleBackColor = false;
            this.CloseButton.Click += new System.EventHandler(this.CloseButton_Click);
            // 
            // LoginIdLavel
            // 
            this.LoginIdLavel.AutoSize = true;
            this.LoginIdLavel.Font = new System.Drawing.Font("メイリオ", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.LoginIdLavel.Location = new System.Drawing.Point(50, 54);
            this.LoginIdLavel.Name = "LoginIdLavel";
            this.LoginIdLavel.Size = new System.Drawing.Size(24, 20);
            this.LoginIdLavel.TabIndex = 6;
            this.LoginIdLavel.Text = "ID";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("メイリオ", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.label1.Location = new System.Drawing.Point(50, 86);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(69, 20);
            this.label1.TabIndex = 7;
            this.label1.Text = "Password";
            // 
            // LoginPasswordText
            // 
            this.LoginPasswordText.BackColor = System.Drawing.Color.White;
            this.LoginPasswordText.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.LoginPasswordText.Location = new System.Drawing.Point(125, 87);
            this.LoginPasswordText.Name = "LoginPasswordText";
            this.LoginPasswordText.Size = new System.Drawing.Size(179, 19);
            this.LoginPasswordText.TabIndex = 1;
            // 
            // LoginIdText
            // 
            this.LoginIdText.BackColor = System.Drawing.Color.White;
            this.LoginIdText.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.LoginIdText.Location = new System.Drawing.Point(125, 55);
            this.LoginIdText.Name = "LoginIdText";
            this.LoginIdText.Size = new System.Drawing.Size(179, 19);
            this.LoginIdText.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("メイリオ", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.label2.Location = new System.Drawing.Point(12, 9);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(87, 20);
            this.label2.TabIndex = 10;
            this.label2.Text = "LOGINFORM";
            // 
            // LoginButton
            // 
            this.LoginButton.BackColor = System.Drawing.Color.LightSlateGray;
            this.LoginButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.LoginButton.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.LoginButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.LoginButton.Location = new System.Drawing.Point(205, 112);
            this.LoginButton.Name = "LoginButton";
            this.LoginButton.Size = new System.Drawing.Size(99, 30);
            this.LoginButton.TabIndex = 2;
            this.LoginButton.Text = "LogIn";
            this.LoginButton.UseVisualStyleBackColor = false;
            this.LoginButton.Click += new System.EventHandler(this.LoginButton_Click);
            // 
            // LoginForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(358, 163);
            this.Controls.Add(this.LoginButton);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.LoginIdText);
            this.Controls.Add(this.LoginPasswordText);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.LoginIdLavel);
            this.Controls.Add(this.CloseButton);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "LoginForm";
            this.Text = "LoginForm";
            this.Load += new System.EventHandler(this.LoginForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button CloseButton;
        private System.Windows.Forms.Label LoginIdLavel;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox LoginPasswordText;
        private System.Windows.Forms.TextBox LoginIdText;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button LoginButton;
    }
}
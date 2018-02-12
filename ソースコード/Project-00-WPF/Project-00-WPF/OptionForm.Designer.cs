namespace Project_00_WPF
{
    partial class OptionForm
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
            this.OptionLavel = new System.Windows.Forms.Label();
            this.ApplyButton = new System.Windows.Forms.Button();
            this.OptionTabControl = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.OptionTabControl.SuspendLayout();
            this.SuspendLayout();
            // 
            // CloseButton
            // 
            this.CloseButton.BackColor = System.Drawing.Color.PaleVioletRed;
            this.CloseButton.FlatAppearance.BorderSize = 0;
            this.CloseButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.CloseButton.Font = new System.Drawing.Font("メイリオ", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.CloseButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.CloseButton.Location = new System.Drawing.Point(571, 0);
            this.CloseButton.Name = "CloseButton";
            this.CloseButton.Size = new System.Drawing.Size(40, 34);
            this.CloseButton.TabIndex = 3;
            this.CloseButton.Text = "✖";
            this.CloseButton.UseVisualStyleBackColor = false;
            // 
            // OptionLavel
            // 
            this.OptionLavel.AutoSize = true;
            this.OptionLavel.Font = new System.Drawing.Font("メイリオ", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.OptionLavel.Location = new System.Drawing.Point(12, 14);
            this.OptionLavel.Name = "OptionLavel";
            this.OptionLavel.Size = new System.Drawing.Size(51, 20);
            this.OptionLavel.TabIndex = 11;
            this.OptionLavel.Text = "Option";
            // 
            // ApplyButton
            // 
            this.ApplyButton.BackColor = System.Drawing.Color.LightSlateGray;
            this.ApplyButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.ApplyButton.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.ApplyButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.ApplyButton.Location = new System.Drawing.Point(500, 339);
            this.ApplyButton.Name = "ApplyButton";
            this.ApplyButton.Size = new System.Drawing.Size(99, 30);
            this.ApplyButton.TabIndex = 12;
            this.ApplyButton.Text = "Apply";
            this.ApplyButton.UseVisualStyleBackColor = false;
            // 
            // OptionTabControl
            // 
            this.OptionTabControl.Controls.Add(this.tabPage1);
            this.OptionTabControl.Controls.Add(this.tabPage2);
            this.OptionTabControl.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.OptionTabControl.Location = new System.Drawing.Point(16, 37);
            this.OptionTabControl.Name = "OptionTabControl";
            this.OptionTabControl.SelectedIndex = 0;
            this.OptionTabControl.Size = new System.Drawing.Size(583, 296);
            this.OptionTabControl.TabIndex = 13;
            // 
            // tabPage1
            // 
            this.tabPage1.Location = new System.Drawing.Point(4, 27);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(575, 265);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "UserTab";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // tabPage2
            // 
            this.tabPage2.Location = new System.Drawing.Point(4, 27);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(575, 265);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "ApplicationTab";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // OptionForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(611, 381);
            this.Controls.Add(this.OptionTabControl);
            this.Controls.Add(this.ApplyButton);
            this.Controls.Add(this.OptionLavel);
            this.Controls.Add(this.CloseButton);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "OptionForm";
            this.Text = "OptionForm";
            this.Load += new System.EventHandler(this.OptionForm_Load);
            this.OptionTabControl.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button CloseButton;
        private System.Windows.Forms.Label OptionLavel;
        private System.Windows.Forms.Button ApplyButton;
        private System.Windows.Forms.TabControl OptionTabControl;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
    }
}
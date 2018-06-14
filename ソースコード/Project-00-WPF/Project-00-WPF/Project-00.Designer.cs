namespace Project_00_WPF
{
    partial class Project00
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージ リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Legend legend1 = new System.Windows.Forms.DataVisualization.Charting.Legend();
            System.Windows.Forms.DataVisualization.Charting.Series series1 = new System.Windows.Forms.DataVisualization.Charting.Series();
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea2 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Legend legend2 = new System.Windows.Forms.DataVisualization.Charting.Legend();
            System.Windows.Forms.DataVisualization.Charting.Series series2 = new System.Windows.Forms.DataVisualization.Charting.Series();
            this.CloseButton = new System.Windows.Forms.Button();
            this.MinimizedButton = new System.Windows.Forms.Button();
            this.TabControl = new System.Windows.Forms.TabControl();
            this.ChartTab = new System.Windows.Forms.TabPage();
            this.ChartGraph = new System.Windows.Forms.DataVisualization.Charting.Chart();
            this.TradeTab = new System.Windows.Forms.TabPage();
            this.TradeGraph = new System.Windows.Forms.DataVisualization.Charting.Chart();
            this.TradeLog = new System.Windows.Forms.TextBox();
            this.TradeLogLabel = new System.Windows.Forms.Label();
            this.StartButton = new System.Windows.Forms.Button();
            this.EndButton = new System.Windows.Forms.Button();
            this.TradingPanel = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.button2 = new System.Windows.Forms.Button();
            this.TabControl.SuspendLayout();
            this.ChartTab.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.ChartGraph)).BeginInit();
            this.TradeTab.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.TradeGraph)).BeginInit();
            this.TradingPanel.SuspendLayout();
            this.SuspendLayout();
            // 
            // CloseButton
            // 
            this.CloseButton.BackColor = System.Drawing.Color.PaleVioletRed;
            this.CloseButton.FlatAppearance.BorderSize = 0;
            this.CloseButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.CloseButton.Font = new System.Drawing.Font("メイリオ", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.CloseButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.CloseButton.Location = new System.Drawing.Point(1286, -1);
            this.CloseButton.Name = "CloseButton";
            this.CloseButton.Size = new System.Drawing.Size(40, 34);
            this.CloseButton.TabIndex = 2;
            this.CloseButton.Text = "✖";
            this.CloseButton.UseVisualStyleBackColor = false;
            this.CloseButton.Click += new System.EventHandler(this.CloseButton_Click);
            // 
            // MinimizedButton
            // 
            this.MinimizedButton.BackColor = System.Drawing.Color.LightSlateGray;
            this.MinimizedButton.FlatAppearance.BorderSize = 0;
            this.MinimizedButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.MinimizedButton.Font = new System.Drawing.Font("メイリオ", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.MinimizedButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.MinimizedButton.Location = new System.Drawing.Point(1247, -1);
            this.MinimizedButton.Name = "MinimizedButton";
            this.MinimizedButton.Size = new System.Drawing.Size(40, 34);
            this.MinimizedButton.TabIndex = 3;
            this.MinimizedButton.Text = "ー";
            this.MinimizedButton.UseVisualStyleBackColor = false;
            this.MinimizedButton.Click += new System.EventHandler(this.MinimizedButton_Click);
            // 
            // TabControl
            // 
            this.TabControl.Controls.Add(this.ChartTab);
            this.TabControl.Controls.Add(this.TradeTab);
            this.TabControl.Location = new System.Drawing.Point(12, 57);
            this.TabControl.Name = "TabControl";
            this.TabControl.SelectedIndex = 0;
            this.TabControl.Size = new System.Drawing.Size(1052, 608);
            this.TabControl.TabIndex = 5;
            // 
            // ChartTab
            // 
            this.ChartTab.Controls.Add(this.ChartGraph);
            this.ChartTab.Location = new System.Drawing.Point(4, 27);
            this.ChartTab.Name = "ChartTab";
            this.ChartTab.Padding = new System.Windows.Forms.Padding(3);
            this.ChartTab.Size = new System.Drawing.Size(1044, 577);
            this.ChartTab.TabIndex = 0;
            this.ChartTab.Text = "Chart";
            this.ChartTab.UseVisualStyleBackColor = true;
            // 
            // ChartGraph
            // 
            this.ChartGraph.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(28)))), ((int)(((byte)(28)))), ((int)(((byte)(28)))));
            chartArea1.BackColor = System.Drawing.Color.Transparent;
            chartArea1.Name = "ChartArea1";
            this.ChartGraph.ChartAreas.Add(chartArea1);
            legend1.Name = "Legend1";
            this.ChartGraph.Legends.Add(legend1);
            this.ChartGraph.Location = new System.Drawing.Point(0, 0);
            this.ChartGraph.Name = "ChartGraph";
            series1.ChartArea = "ChartArea1";
            series1.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            series1.Color = System.Drawing.Color.Lime;
            series1.Legend = "Legend1";
            series1.Name = "Series1";
            this.ChartGraph.Series.Add(series1);
            this.ChartGraph.Size = new System.Drawing.Size(1041, 576);
            this.ChartGraph.TabIndex = 0;
            this.ChartGraph.Text = "chart1";
            // 
            // TradeTab
            // 
            this.TradeTab.Controls.Add(this.TradeGraph);
            this.TradeTab.Location = new System.Drawing.Point(4, 27);
            this.TradeTab.Name = "TradeTab";
            this.TradeTab.Padding = new System.Windows.Forms.Padding(3);
            this.TradeTab.Size = new System.Drawing.Size(1044, 577);
            this.TradeTab.TabIndex = 1;
            this.TradeTab.Text = "Trade";
            this.TradeTab.UseVisualStyleBackColor = true;
            // 
            // TradeGraph
            // 
            chartArea2.Name = "ChartArea1";
            this.TradeGraph.ChartAreas.Add(chartArea2);
            legend2.Name = "Legend1";
            this.TradeGraph.Legends.Add(legend2);
            this.TradeGraph.Location = new System.Drawing.Point(0, 0);
            this.TradeGraph.Name = "TradeGraph";
            series2.ChartArea = "ChartArea1";
            series2.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            series2.Legend = "Legend1";
            series2.Name = "Series1";
            this.TradeGraph.Series.Add(series2);
            this.TradeGraph.Size = new System.Drawing.Size(1020, 576);
            this.TradeGraph.TabIndex = 1;
            this.TradeGraph.Text = "chart1";
            // 
            // TradeLog
            // 
            this.TradeLog.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.TradeLog.Location = new System.Drawing.Point(1070, 89);
            this.TradeLog.Multiline = true;
            this.TradeLog.Name = "TradeLog";
            this.TradeLog.ReadOnly = true;
            this.TradeLog.Size = new System.Drawing.Size(243, 576);
            this.TradeLog.TabIndex = 6;
            // 
            // TradeLogLabel
            // 
            this.TradeLogLabel.AutoSize = true;
            this.TradeLogLabel.Location = new System.Drawing.Point(1070, 68);
            this.TradeLogLabel.Name = "TradeLogLabel";
            this.TradeLogLabel.Size = new System.Drawing.Size(62, 18);
            this.TradeLogLabel.TabIndex = 7;
            this.TradeLogLabel.Text = "TradeLog";
            // 
            // StartButton
            // 
            this.StartButton.BackColor = System.Drawing.Color.CornflowerBlue;
            this.StartButton.FlatAppearance.BorderSize = 0;
            this.StartButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.StartButton.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.StartButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.StartButton.Location = new System.Drawing.Point(6, 16);
            this.StartButton.Name = "StartButton";
            this.StartButton.Size = new System.Drawing.Size(140, 25);
            this.StartButton.TabIndex = 0;
            this.StartButton.Text = "Start";
            this.StartButton.UseVisualStyleBackColor = false;
            this.StartButton.Click += new System.EventHandler(this.StartButton_Click);
            // 
            // EndButton
            // 
            this.EndButton.BackColor = System.Drawing.Color.PaleVioletRed;
            this.EndButton.FlatAppearance.BorderSize = 0;
            this.EndButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.EndButton.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.EndButton.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.EndButton.Location = new System.Drawing.Point(146, 16);
            this.EndButton.Name = "EndButton";
            this.EndButton.Size = new System.Drawing.Size(140, 25);
            this.EndButton.TabIndex = 1;
            this.EndButton.Text = "End";
            this.EndButton.UseVisualStyleBackColor = false;
            // 
            // TradingPanel
            // 
            this.TradingPanel.Controls.Add(this.label1);
            this.TradingPanel.Controls.Add(this.button2);
            this.TradingPanel.Controls.Add(this.EndButton);
            this.TradingPanel.Controls.Add(this.StartButton);
            this.TradingPanel.Location = new System.Drawing.Point(7, 12);
            this.TradingPanel.Name = "TradingPanel";
            this.TradingPanel.Size = new System.Drawing.Size(1234, 47);
            this.TradingPanel.TabIndex = 4;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(7, -4);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(68, 18);
            this.label1.TabIndex = 8;
            this.label1.Text = "Project-00";
            // 
            // button2
            // 
            this.button2.BackColor = System.Drawing.Color.LightSlateGray;
            this.button2.FlatAppearance.BorderSize = 0;
            this.button2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.button2.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.button2.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.button2.Location = new System.Drawing.Point(286, 16);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(140, 25);
            this.button2.TabIndex = 1;
            this.button2.Text = "Option";
            this.button2.UseVisualStyleBackColor = false;
            // 
            // Project00
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(1325, 677);
            this.Controls.Add(this.TradeLogLabel);
            this.Controls.Add(this.TradeLog);
            this.Controls.Add(this.TabControl);
            this.Controls.Add(this.TradingPanel);
            this.Controls.Add(this.MinimizedButton);
            this.Controls.Add(this.CloseButton);
            this.Font = new System.Drawing.Font("メイリオ", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.Name = "Project00";
            this.Text = "Project-00 Trading";
            this.Load += new System.EventHandler(this.Project00_Load);
            this.TabControl.ResumeLayout(false);
            this.ChartTab.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.ChartGraph)).EndInit();
            this.TradeTab.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.TradeGraph)).EndInit();
            this.TradingPanel.ResumeLayout(false);
            this.TradingPanel.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button CloseButton;
        private System.Windows.Forms.Button MinimizedButton;
        private System.Windows.Forms.TabControl TabControl;
        private System.Windows.Forms.TabPage ChartTab;
        private System.Windows.Forms.DataVisualization.Charting.Chart ChartGraph;
        private System.Windows.Forms.TabPage TradeTab;
        private System.Windows.Forms.DataVisualization.Charting.Chart TradeGraph;
        private System.Windows.Forms.TextBox TradeLog;
        private System.Windows.Forms.Label TradeLogLabel;
        private System.Windows.Forms.Button StartButton;
        private System.Windows.Forms.Button EndButton;
        private System.Windows.Forms.Panel TradingPanel;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Label label1;
    }
}


#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //error tag set blank
    ui->errorLabel->setText("");
    // sets number of columns to 2
    ui->tableWidget->setColumnCount(21);
    // initialize number of rows
    ui->tableWidget->setRowCount(0);
    // create table headers
    ui->tableWidget->setHorizontalHeaderItem(0, new QTableWidgetItem("Altered File Name"));
    ui->tableWidget->setHorizontalHeaderItem(1, new QTableWidgetItem("Unaltered File Name"));
    ui->tableWidget->setHorizontalHeaderItem(2, new QTableWidgetItem("Content Type"));
    ui->tableWidget->setHorizontalHeaderItem(3, new QTableWidgetItem("Title"));
    ui->tableWidget->setHorizontalHeaderItem(4, new QTableWidgetItem("Episode Name"));
    ui->tableWidget->setHorizontalHeaderItem(5, new QTableWidgetItem("Ripping Group"));
    ui->tableWidget->setHorizontalHeaderItem(6, new QTableWidgetItem("Season(s)"));
    ui->tableWidget->setHorizontalHeaderItem(7, new QTableWidgetItem("Episode(s)"));
    ui->tableWidget->setHorizontalHeaderItem(8, new QTableWidgetItem("Batch"));
    ui->tableWidget->setHorizontalHeaderItem(9, new QTableWidgetItem("Resolution"));
    ui->tableWidget->setHorizontalHeaderItem(10, new QTableWidgetItem("Video Tags"));
    ui->tableWidget->setHorizontalHeaderItem(11, new QTableWidgetItem("Audio Tags"));
    ui->tableWidget->setHorizontalHeaderItem(12, new QTableWidgetItem("Audio Format"));
    ui->tableWidget->setHorizontalHeaderItem(13, new QTableWidgetItem("Audio Language"));
    ui->tableWidget->setHorizontalHeaderItem(14, new QTableWidgetItem("Subtitle Tags"));
    ui->tableWidget->setHorizontalHeaderItem(15, new QTableWidgetItem("Day"));
    ui->tableWidget->setHorizontalHeaderItem(16, new QTableWidgetItem("Month"));
    ui->tableWidget->setHorizontalHeaderItem(17, new QTableWidgetItem("Year"));
    ui->tableWidget->setHorizontalHeaderItem(18, new QTableWidgetItem("Revision Number"));
    ui->tableWidget->setHorizontalHeaderItem(19, new QTableWidgetItem("File Type"));
    ui->tableWidget->setHorizontalHeaderItem(20, new QTableWidgetItem("Checksum"));

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_searchButton_clicked()
{
    //error tag set blank
    ui->errorLabel->setText("");
    QString test = ui->textEdit->toPlainText();
    qInfo(qPrintable(test));
    if(!test.trimmed().isEmpty() && (ui->tvButton->isChecked() || ui->moviesButton->isChecked()))
    {
        // IN - check radio buttons
        QString movietv;
        if(ui->tvButton->isChecked())
            movietv = "s";
        else
            movietv = "m";
        // STORE - command to be run with grabbed text
        QString cmd_qt = QString("python SearchQuery.py " + movietv + " \"" + test + "\"");
        // OUT - test output for command
        qInfo(qPrintable(cmd_qt));
        // RUN - runs command
        int q = system(qPrintable(cmd_qt));
        // OUT - outputs command result
        qInfo( qPrintable( QString::number(q)));

        //resets table
        ui->tableWidget->setRowCount(0);
        // IN - read in search data from file
        QFile inFile("results.txt");
        if (inFile.open(QIODevice::ReadOnly))
        {
           QTextStream in(&inFile);
           while (!in.atEnd())
           {
               ui->tableWidget->insertRow ( ui->tableWidget->rowCount() );
               ui->tableWidget->setItem   ( ui->tableWidget->rowCount()-1, 0, new QTableWidgetItem(in.readLine()));
               ui->tableWidget->setItem   ( ui->tableWidget->rowCount()-1, 1, new QTableWidgetItem(in.readLine()));
               if(movietv == "m")
                   ui->tableWidget->setItem(ui->tableWidget->rowCount()-1, 2, new QTableWidgetItem("Movie"));
               else
                   ui->tableWidget->setItem(ui->tableWidget->rowCount()-1, 2, new QTableWidgetItem("Series"));
           }
           inFile.close();
        }
    }
    else
    {
        //error tag set blank
        ui->errorLabel->setText("Error");
    }
}

void MainWindow::on_saveButton_clicked()
{
    QFile outfile("AITestFile.csv");
    if(ui->tableWidget->rowCount() > 0)
    {
        if(outfile.open(QIODevice::WriteOnly | QIODevice::Append))
        {
            bool write;
            int cc = ui->tableWidget->columnCount();
            int rc = ui->tableWidget->rowCount();
            QTextStream stream(&outfile);

            for(int i = 0; i < rc; i++)
            {
                write = false;
                //check to see if we should write
                for(int j = 3; j < cc && !write; j++)
                {
                    //IF - text box not empty
                    QTableWidgetItem* node = ui->tableWidget->item(i, j);
                    if(node)
                    {
                        qInfo( qPrintable( node->text() ));
                        write = true;
                    }
                }

                //IF - write is true then we write line to file
                if(write)
                {
                    for(int j = 0; j < cc; j++)
                    {

                        QTableWidgetItem* node2 = ui->tableWidget->item(i, j);
                        //IF - node is not empty
                        if(node2)
                        {
                            QString str = node2->text();
                            if(str.contains('|'))
                            {
                                //replace spaces with |
                                str.push_back('\"');
                                str.push_front('\"');
                            }
                            stream << str;
                        }
                        if(j < cc-1)
                             stream << "|";
                        else
                            stream << "\n";
                    }
                }
            }
        }
        outfile.close();
    }
    else
    {
        QString cmd_qt = QString(".\\direc.bat");
        // OUT - test output for command
        qInfo(qPrintable(cmd_qt));
        // RUN - runs command
        int q = system(qPrintable(cmd_qt));
        // OUT - outputs command result
        qInfo( qPrintable( QString::number(q)));
    }
}

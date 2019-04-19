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
    ui->tableWidget->setColumnCount(3);
    // initialize number of rows
    ui->tableWidget->setRowCount(0);
    // create table headers
    ui->tableWidget->setHorizontalHeaderItem(0, new QTableWidgetItem("Results"));
    ui->tableWidget->setHorizontalHeaderItem(1, new QTableWidgetItem("Link"));
    ui->tableWidget->setHorizontalHeaderItem(2, new QTableWidgetItem("Final Parsed"));

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
    if(!test.trimmed().isEmpty())
    {
        //command to be run with grabbed text
        QString cmd_qt = QString("py \"C:\\Users\\Chris Baroni\\Documents\\481AI\\project\\Xanadu\\Xanadu_Parse.py\" %1").arg(test);
        // test output for command
        qInfo(qPrintable(cmd_qt));
        //runs command
        int q = system(qPrintable(cmd_qt));
        // outputs command result
        qInfo( qPrintable( QString::number(q)));

        //resets table
        ui->tableWidget->setRowCount(0);
        //read in search data from file
        QFile inFile("results.txt");
        if (inFile.open(QIODevice::ReadOnly))
        {
           QTextStream in(&inFile);
           while (!in.atEnd())
           {
               ui->tableWidget->insertRow ( ui->tableWidget->rowCount() );
               ui->tableWidget->setItem   ( ui->tableWidget->rowCount()-1, 0, new QTableWidgetItem(in.readLine()));
               ui->tableWidget->setItem   ( ui->tableWidget->rowCount()-1, 1, new QTableWidgetItem(in.readLine()));
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

void MainWindow::on_extraButton_clicked()
{

}

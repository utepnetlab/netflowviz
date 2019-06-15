/*
Author: Carlos Alcantara
Node JS server for Data Visualization plot creation with python scripts
Version 2.0

supports SQL table filtering
	- SQL table name "netflowData"
	- Only SELECT statement is supported with the WHERE modifier
NetFlow Data Visualizations
	- Univariate
	- Multivariate
	- Scatterplot Matrix
	- Bivariate Distribution
	- Geospatial
	- DrillDown using interactive heatmaps
*/

// Load modules
var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var fs = require('fs');
var execSync = require('sync-exec');
var app = express();
var source, dest;

// View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Body Parser Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// Set Static Path
app.use(express.static(path.join(__dirname, 'public')))

// Start server
app.listen(62432, function(){
	console.log('Server Stated on port 62432...');
});

// Render index html (Homepage) to client
app.get('/', 
	function(req, res){
	var csv = [];
	var temp = [];

	// Reads filenames in "csv/" directory and populates the dropdown menu
	temp = fs.readdirSync('csv/'	);
	for (var i = 0; i<temp.length; i++) {
			if (temp[i].charAt(0) != '.'){
				csv.push(temp[i]);
			}
		}
	res.render('index',{csv:csv});
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////// Univariate Tab //////////////////////////////////////////////////////

// Univariate tab 
app.post('/univariate', function(req, res){
	var file = req.body.univariateFile;
	var field = req.body.field;
	var style = req.body.style;
	var sqloption = req.body.univariateSQLoption;
	var sqlfilter = req.body.univariateSQLfilter;
	const execSync = require('child_process').execSync;
	
	// check if SQL filter selected and call python subprocess to generate visualization
	if (sqloption == 'true')
	{
		console.log('univariate.py '+file+' '+field+' '+style+' "'+sqloption+'" "'+sqlfilter+'"');
		var process = execSync('python py/univariate.py '+file+' '+field+' '+style+' "'+sqloption+'" "'+sqlfilter+'"');
	}
	else
	{
		console.log('univariate.py '+file+' '+field+' '+style+' "'+sqloption+'"');
		var process = execSync('python py/univariate.py '+file+' '+field+' '+style+' "'+sqloption+'"');
	}
	
	// Read image and send to res object
	fs.readFile('images/univariate.svg', function(err, data) {
		if (err) throw err;
		res.write(data);
		res.end();
	});
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////// Multivariate Tab /////////////////////////////////////////////////////

// Multivariate
app.post('/multivariate', function(req, res){
	var file = req.body.multivariateFile;
	var xAxis = req.body.xAxis;
	var yAxis = req.body.yAxis;
	var zAxis = req.body.zAxis;
	var dotSize = req.body.dotSize;
	var sqloption = req.body.multivariateSQLoption;
	var sqlfilter = req.body.multivariateSQLfilter;
	const execSync = require('child_process').execSync;
	
	// check if SQL filter selected and call python subprocess to generate visualization
	if (sqloption == 'true')
	{
		console.log('python multivariate.py '+file+' '+xAxis+' '+yAxis+' '+zAxis+' '+dotSize+' "'+sqloption+'" "'+sqlfilter+'"');
		var process = execSync('python py/multivariate.py '+file+' '+xAxis+' '+yAxis+' '+zAxis+' '+dotSize+' "'+sqloption+'" "'+sqlfilter+'"');
	}
	else
	{
		console.log('python multivariate.py '+file+' '+xAxis+' '+yAxis+' '+zAxis+' '+dotSize+' "'+sqloption+'"');
		var process = execSync('python py/multivariate.py '+file+' '+xAxis+' '+yAxis+' '+zAxis+' '+dotSize+' "'+sqloption+'"');
	}

	// Read image and send to res object
	fs.readFile('images/multivariate.svg', function(err, data) {
		if (err) throw err;
		res.write(data);
		res.end();
	});
});


// Scatter Plot Matix
app.post('/scatterplot', function(req, res){
	console.log(req.body);
	var file = req.body.scatterplotFile;
	var sqloption = req.body.scatterplotSQLoption;
	var sqlfilter = req.body.scatterplotSQLfilter;
	const execSync = require('child_process').execSync;
	
	
	//////////////////////////
	var featuresList='';
	for (i in req.body.plotOption) {
    	featuresList += req.body.plotOption[i].toString()+' ';
	}
	featuresList = featuresList.slice(0,-1);
	///////////////////////////
	
	// check if SQL filter selected and call python subprocess to generate visualization
	if (sqloption == 'true')
	{
		console.log('python scatterplot.py '+file+' "'+sqloption+'" "'+sqlfilter+'" '+featuresList);
		var process = execSync('python py/scatterplot.py '+file+' "'+sqloption+'" "'+sqlfilter+'" '+featuresList);
	}
	else
	{
		console.log('python scatterplot.py '+file+' "'+sqloption+'" '+featuresList);
		var process = execSync('python py/scatterplot.py '+file+' "'+sqloption+'" '+featuresList);
	}
	
	// Read image and send to res object
	fs.readFile('images/scatterplot.svg', function(err, data) {
		if (err) throw err;
		res.write(data);
		res.end();
	});
});


// Bivariate Distribution
app.post('/bivariate', function(req, res){
	console.log(req.body);
	var file = req.body.bivariateFile;
	var sqloption = req.body.bivariateSQLoption;
	var sqlfilter = req.body.bivariateSQLfilter;
	var xAxis = req.body.bivariateAxisX;
	var yAxis = req.body.bivariateAxisY;
	const execSync = require('child_process').execSync;

	// check if SQL filter selected and call python subprocess to generate visualization
	if (sqloption == 'true')
	{
		console.log('python bivariate.py '+file+' '+xAxis+' '+yAxis+' "'+sqloption+'" "'+sqlfilter+'"');
		var process = execSync('python py/bivariate.py '+file+' '+xAxis+' '+yAxis+' "'+sqloption+'" "'+sqlfilter+'"');
	}
	else
	{
		console.log('python bivariate.py '+file+' '+xAxis+' '+yAxis+' "'+sqloption+'"');
		var process = execSync('python py/bivariate.py '+file+' '+xAxis+' '+yAxis+' "'+sqloption+'"');
	}
	console.log('ran python script');
	
	// Read image and send to res object
	fs.readFile('images/bivariate.svg', function(err, data) {
		if (err) throw err;
		res.write(data);
		res.end();
	});
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////// Geo-spatial Tab /////////////////////////////////////////////////////

// Create map request to send to python script
app.post('/geo', function(req, res){
	filter = req.body.geoSQLfilter;
	if (filter == undefined)
		filter = 'false';
	if (filter != 'false')
		filter = filter.replace(new RegExp(" ", 'g'), '_');
	colorFilter = req.body.colorLineCheck;
	if (colorFilter != 'true')
		colorFilter = 'false';
	var json =	{
					"file":req.body.geoFile,
					"defaultColor":req.body.defaultColor,
					"plotType":req.body.plotType,
					"plotX":req.body.geoAxisX,
					"plotY":req.body.geoAxisY,
					"popupLen":req.body.popupLen,
					"sortvar":req.body.sortvar,
					"getMarkerLogos":req.body.markerLogos,
					"aggregate":req.body.aggregation,
					"colorFilter":colorFilter,
					"columnName":req.body.columnName,
					"condition":req.body.condition,
					"conditionalValue":req.body.conditionalValue,
					"conditionalColor":req.body.conditionalColor,
					"filter":filter
					};
	jsonstr = JSON.stringify(json);
	jsonstr = jsonstr.replace(new RegExp('\"', 'g'), '\\\"');
	const execSync = require('child_process').execSync;
	console.log('python py/mapDriver.py '+ JSON.stringify(json));
	var process = execSync('python py/mapDriver.py '+jsonstr);

	res.render('tempMap.ejs')
});

// // Create map popup chart
// app.post('/mapChart', function(req, res){
// 	var body = req.body;
// 	const execSync = require('child_process').execSync;
// 	var process = execSync('python py/onDemand.py "'+body.csv+'" '+body.lat1+' '+body.lon1+' '+body.lat2+' '+body.lon2);
	
// 	// Read file and send chart response to res object
// 	fs.readFile('popup.txt', function(err, data) {
// 		if (err) throw err;
// 		res.write(data);
// 		res.end();
// 	});
// });




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////// Bokeh Drilldown /////////////////////////////////////////////////////

// Create continent level heatmap
app.post('/continent', function(req, res){
	var file = req.body.drilldownFile;
	const execSync = require('child_process').execSync;
	var process = execSync('python py/continent.py csv/'+file);
	console.log('python continent.py csv/'+file);

	res.render('continent.ejs');
});

// Create country level heatmap
app.post('/country', function (req, res){
	var file = req.body.FileName;
	var srcVal = req.body.SrcVal;
	var destVal = req.body.DestVal;

	const execSync = require('child_process').execSync;
	var process = execSync('python py/drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" views/country.ejs');
	console.log('python drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" views/country.ejs');

	res.render('country.ejs');
 });

// Create organization level heatmap
app.post('/org', function (req, res){
	var file = req.body.FileName;
	var srcVal = req.body.SrcVal;
	var destVal = req.body.DestVal;

	const execSync = require('child_process').execSync;
	var process = execSync('python py/drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" views/org.ejs');
	console.log('python drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" views/org.ejs');

	res.render('org.ejs');
 });

// Create bottom level histogram comparing data between two organizations
app.post('/asHist', function (req, res){
	file = req.body.FileName;
	srcVal = req.body.SrcVal;
	destVal = req.body.DestVal;

	const execSync = require('child_process').execSync;
	var process = execSync('python py/drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" "views/hist.ejs"');
	console.log('python drilldownDriver.py '+file+' "'+srcVal+'" "'+destVal+'" "views/hist.ejs"');

	res.render('hist.ejs');
 });

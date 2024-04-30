using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using OdataAPI.Data;
using System.Data.SqlClient;
using OdataAPI.Controllers;
using Microsoft.AspNetCore.OData;
using Microsoft.OData.Edm;
using Microsoft.OData.ModelBuilder;
using OdataAPI.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<AlphaAnalyticsDbContext>(options =>
{
    var connectionBuilder = new SqlConnectionStringBuilder();
    //connectionBuilder.DataSource = "DESKTOP-6T987U5";
    //connectionBuilder.InitialCatalog = "AlphaAnalytics";
    //connectionBuilder.UserID = "govind";
    //connectionBuilder.Password = "test@123"; 
    options.UseSqlite("Data Source=.\\Data\\alphaanalytics.db");
});
static IEdmModel GetEdmModel()
{
    ODataConventionModelBuilder builder = new ODataConventionModelBuilder();
    builder.EntitySet<Country>("countries");
    builder.EntitySet<Product>("products");
    builder.EntitySet<Flow>("flows");
    builder.EntitySet<DataValue>("values");
    builder.EntitySet<Year>("years");
    return builder.GetEdmModel();
}
builder.Services.AddControllers().AddOData(options => options
       .AddRouteComponents("odata", GetEdmModel())
       .Select()
       .Filter()
       .OrderBy()
       .SetMaxTop(20)
       .Count()
       .Expand()
);
var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using OdataAPI.Data;
using OdataAPI.Models;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace OdataAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductsController : ODataController
    {
        private readonly AlphaAnalyticsDbContext _context;

        public ProductsController(AlphaAnalyticsDbContext context)
        {
            _context = context;
        }

        // GET: api/<ProductsController>
        [EnableQuery]
        [HttpGet]
        public async Task<IQueryable<Product>> GetAsync()
        {
            return _context.Products;
        }
    }
}

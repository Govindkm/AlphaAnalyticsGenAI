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
    public class CountriesController : ODataController
    {
        private readonly AlphaAnalyticsDbContext _context;

        public CountriesController(AlphaAnalyticsDbContext context)
        {
            _context = context;
        }

        // GET: api/<CountriesController>
        /// <summary>
        /// Gets the list of countries that have product sales
        /// </summary>
        /// <returns>List of countries</returns>
        [EnableQuery]
        [HttpGet]
        public async Task<IQueryable<Country>> Get()
        {
            return _context.Countries;
        }       
    }
}

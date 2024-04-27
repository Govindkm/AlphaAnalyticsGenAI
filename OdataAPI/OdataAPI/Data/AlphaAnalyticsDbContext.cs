using Microsoft.EntityFrameworkCore;
using OdataAPI.Models;

namespace OdataAPI.Data
{
    public class AlphaAnalyticsDbContext: DbContext
    {
        public DbSet<Year> Years { get; set; }
        public DbSet<Country> Countries { get; set; }
        public DbSet<Flow> Flows { get; set; }
        public DbSet<Product> Products { get; set; }
        public DbSet<DataValue> DataValues { get; set; }
    }
}

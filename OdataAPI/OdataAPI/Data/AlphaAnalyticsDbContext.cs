using Microsoft.EntityFrameworkCore;
using OdataAPI.Models;

namespace OdataAPI.Data
{
    public class AlphaAnalyticsDbContext: DbContext
    {
        public AlphaAnalyticsDbContext(DbContextOptions options): base(options)
        { }
        public DbSet<Year> Years { get; set; }
        public DbSet<Country> Countries { get; set; }
        public DbSet<Flow> Flows { get; set; }
        public DbSet<Product> Products { get; set; }
        public DbSet<DataValue> DataValues { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<DataValue>()
                .HasOne(d => d.Country)
                .WithMany(c => c.DataValues)
                .HasForeignKey(d => d.CountryID);

            modelBuilder.Entity<DataValue>()
                .HasOne(d => d.Product)
                .WithMany(p => p.DataValues)
                .HasForeignKey(d => d.ProductID);

            modelBuilder.Entity<DataValue>()
                .HasOne(d => d.Year)
                .WithMany(y => y.DataValues)
                .HasForeignKey(d => d.YearID);

            modelBuilder.Entity<DataValue>()
                .HasOne(d => d.Flow)
                .WithMany(f => f.DataValues)
                .HasForeignKey(d => d.FlowID);
        }
    }
}

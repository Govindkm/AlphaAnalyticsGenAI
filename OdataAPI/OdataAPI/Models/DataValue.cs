using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace OdataAPI.Models
{
    [Table("DataValues")]
    public class DataValue
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int DataValueID { get; set; }

        public int? CountryID { get; set; }

        public int? ProductID { get; set; }

        public int? FlowID { get; set; }

        public int? YearID { get; set; }

        public decimal? Value { get; set; }

        // Navigation properties for foreign keys
        public Country Country { get; set; }

        public Product Product { get; set; }

        public Flow Flow { get; set; }

        public Year Year { get; set; }
    }
}

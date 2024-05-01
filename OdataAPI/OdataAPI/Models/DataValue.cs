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

        public int CountryID { get; set; }

        public int ProductID { get; set; }

        public int FlowID { get; set; }

        public int YearID { get; set; }

        public float Value { get; set; }
    }
}

using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace OdataAPI.Models
{
    [Table("Years")]
    public class Year
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int YearId { get; set; }
        public int YearValue { get; set; }

        //Navigation Property
        public ICollection<DataValue> DataValues { get; set; }
    }
}

// Models/NewsItem.cs
using System;
using System.ComponentModel.DataAnnotations;

namespace NewsParserServer.Models
{
    public class NewsItem
    {
        public int Id { get; set; }

        [Required]
        public string Title { get; set; }

        public string Content { get; set; }

        [Required]
        public string Url { get; set; }

        public string Source { get; set; }

        public DateTime PublishedDate { get; set; }

        public DateTime CreatedAt { get; set; }

        public string Category { get; set; }
    }
}
// Data/NewsDbContext.cs
using System.Collections.Generic;
using System.Reflection.Emit;
using Microsoft.EntityFrameworkCore;
using NewsParserServer.Models;

namespace NewsParserServer.Data
{
    public class NewsDbContext : DbContext
    {
        public NewsDbContext(DbContextOptions<NewsDbContext> options) : base(options) { }
        public DbSet<NewsItem> News { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<NewsItem>()
                .HasIndex(n => n.Url)
                .IsUnique();

            modelBuilder.Entity<NewsItem>()
                .Property(n => n.CreatedAt)
                .HasDefaultValueSql("GETDATE()");
        }
    }
}
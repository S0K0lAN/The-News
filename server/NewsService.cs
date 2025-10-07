using Microsoft.EntityFrameworkCore;
using NewsParserServer.Data;
using NewsParserServer.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace NewsParserServer.Services
{
    public class NewsService : INewsService
    {
        private readonly NewsDbContext _context;

        public NewsService(NewsDbContext context)
        {
            _context = context;
        }

        public async Task<bool> SaveNewsAsync(List<NewsItem> newsItems)
        {
            try
            {
                foreach (var newsItem in newsItems)
                {
                    // Проверяем, существует ли уже новость с таким URL
                    var existingNews = await _context.News
                        .FirstOrDefaultAsync(n => n.Url == newsItem.Url);

                    if (existingNews == null)
                    {
                        newsItem.CreatedAt = DateTime.UtcNow;
                        _context.News.Add(newsItem);
                    }
                    else
                    {
                        // Обновляем существующую запись (опционально)
                        existingNews.Title = newsItem.Title;
                        existingNews.Content = newsItem.Content;
                        existingNews.Category = newsItem.Category;
                        _context.News.Update(existingNews);
                    }
                }

                await _context.SaveChangesAsync();
                return true;
            }
            catch (Exception ex)
            {
                // Логирование ошибки
                Console.WriteLine($"Error saving news: {ex.Message}");
                return false;
            }
        }

        public async Task<List<NewsItem>> GetNewsAsync()
        {
            return await _context.News
                .OrderByDescending(n => n.PublishedDate)
                .ToListAsync();
        }
    }
}
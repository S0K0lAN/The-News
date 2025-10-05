// Services/INewsService.cs
using NewsParserServer.Data;
using NewsParserServer.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace NewsParserServer.Services
{
    public interface INewsService
    {
        Task<bool> SaveNewsAsync(List<NewsItem> newsItems);
        Task<List<NewsItem>> GetNewsAsync();
    }
}

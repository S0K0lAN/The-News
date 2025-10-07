// Controllers/NewsController.cs
using Microsoft.AspNetCore.Mvc;
using NewsParserServer.Models;
using NewsParserServer.Services;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace NewsParserServer.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class NewsController : ControllerBase
    {
        private readonly INewsService _newsService;

        public NewsController(INewsService newsService)
        {
            _newsService = newsService;
        }

        [HttpPost("upload")]
        public async Task<IActionResult> UploadNews([FromBody] List<NewsItem> newsItems)
        {
            if (newsItems == null || newsItems.Count == 0)
            {
                return BadRequest("No news items provided");
            }

            var result = await _newsService.SaveNewsAsync(newsItems);

            if (result)
            {
                return Ok(new { message = $"Successfully processed {newsItems.Count} news items" });
            }
            else
            {
                return StatusCode(500, "Error saving news to database");
            }
        }

        [HttpGet]
        public async Task<ActionResult<List<NewsItem>>> GetNews()
        {
            var news = await _newsService.GetNewsAsync();
            return Ok(news);
        }

        [HttpPost("single")]
        public async Task<IActionResult> UploadSingleNews([FromBody] NewsItem newsItem)
        {
            if (newsItem == null)
            {
                return BadRequest("No news item provided");
            }

            var result = await _newsService.SaveNewsAsync(new List<NewsItem> { newsItem });

            if (result)
            {
                return Ok(new { message = "News item saved successfully" });
            }
            else
            {
                return StatusCode(500, "Error saving news to database");
            }
        }
    }
}
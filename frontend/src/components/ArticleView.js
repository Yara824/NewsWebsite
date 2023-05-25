/*
    Article  component that fetches the article a user selected and displays it to the user
*/
import React, {useState, useEffect} from 'react'
//import React from 'react'
import {Input, Grid} from 'semantic-ui-react'

import {
    Container,
    Card,
    Image,
    Menu,
    MenuItem,
    Header,
} from 'semantic-ui-react'
import axios from 'axios'
import './css/ArticleView.css'
import {useNavigate, createSearchParams} from 'react-router-dom'
import ReactHtmlParser from 'react-html-parser'
import useWindowDimensions from './hooks/UseWindowDimensions'
import get_id from './hooks/GetId'
import get_article_id from './hooks/GetArticleId'


export default function Article({navigation}) {
    const [data, setData] = useState({})
    const article = data
    const {width} = useWindowDimensions()


    //function to determine css styling dependent on screen size
    function determineClassName() {
        if (width > 500) {
            return [
                'title_custom_desktop',
                'articleteaser_desktop',
                'articletext_desktop',
            ]
        } else {
            return [
                'title_custom_mobile',
                'articleteaser_mobile',
                'articletext_mobile',
            ]
        }
    }

    const title = determineClassName()[0]
    const teaser = determineClassName()[1]
    const text = determineClassName()[2]

    //retrieving an individual article from API
    useEffect(() => {
        const user_id = new URLSearchParams(window.location.search).get('id')
        const article_id = new URLSearchParams(window.location.search).get(
            'article_id'
        )
        const condition = new URLSearchParams(window.location.search).get(
            'condition'
        )
        const title = new URLSearchParams(window.location.search).get('title')
        const API = process.env.REACT_APP_NEWSAPP_API
        axios
            .get(`${API == null ? 'http://localhost:5000' : API}/article`, {
                params: {user_id, article_id, condition, title},
            })
            .then((res) => setData(res.data[0]))
    }, [])

    const id = get_article_id()
    const image_id = require(`./images/i${id}.png`)
    const InputExampleInput = () => <Input placeholder='Search...'/>

    //on-click function for navigating to the next set of recommendations
    const navigate = useNavigate()

    const navigateToNewsfeed = () => {
        const params = {
            id: get_id(),
            article_id: get_article_id(),
            condition: new URLSearchParams(window.location.search).get('condition'),
            title: new URLSearchParams(window.location.search).get('title'),
        }
        navigate({
            pathname: '/recommendations',
            search: `?${createSearchParams(params)}`,
        })
    }
    const src = require(`./images/i1a.png`)
    const src2 = require(`./images/i2a.png`)
    const src3 = require(`./images/i5d.png`)

    //article display
    return (

        <div>

            <div style={{width: width - 10}}>
                <Menu size="massive">
                    <MenuItem header>Nieuwslijstje.nl</MenuItem>
                    <MenuItem
                        className="article_menu"
                        name="Terug naar de Homepage"
                        icon="home"
                        onClick={navigateToNewsfeed}
                    ></MenuItem>
                </Menu>
            </div>
            <Grid columns={2}>
                <Grid.Column floated='left' width={6}>

                    <div
                        className="ui vertical menu"
                        style={{height: '920px', margin: '0px -20px 0px 5px'}}><a
                        className="item "
                        href="http://localhost:3000/article/?id=490&article_id=1a&title=Transpersonen+over+belang+nieuwe+wet%3A+%E2%80%9CBelachelijk%2C+ik+moet+nu+e
                erst+bewijzen+dat+ik+trans+genoeg+ben%E2%80%9D&condition=condition5"
                        style={{padding: '1em .5em 1em 0.5em'}}>
                        <Image src={src}
                               width="200" height="200" style={{padding: '0.5em 4px 15px 3px'}}></Image>
                        <h5 style={{margin: '1px'}}>Transpersonen over belang nieuwe wet: “Belachelijk, ik moet nu eerst
                            bewijzen dat
                            ik trans genoeg ben</h5></a>
                        <a className="item" href="http://localhost:3000/article/?id=490&article_id=2a&title=Kritiek+op+nieuwe+Transgenderwet+is+%E2%80%9Cboosmakend+en+transfo
                        ob%E2%80%9D%3A+Transvrouw+vertelt+over+het+belang+van+de+wet&condition=condition5"
                           style={{padding: '1em .5em 1em .5em'}}>
                            <Image src={src2}
                                   width="200" height="200" style={{padding: '0.5em 4px 15px 3px'}}></Image>
                            <h5 style={{margin: '1px'}}> Kritiek op nieuwe Transgenderwet is “boosmakend en transfoob”:
                                Transvrouw vertelt over het
                                belang van de wet</h5></a>
                        <a className="item"
                           href="http://localhost:3000/article/?id=490&article_id=5d&title=Kabinet+maakt+publiekelijk+excuses+voor+oude+Tran
                           sgenderwet&condition=condition5"
                           style={{padding: '1em .5em 1em .5em'}}>
                            <Image src={src3}
                                   width="200" height="200" style={{padding: '0.5em 4px 15px 3px'}}></Image>
                            <h5 style={{margin: '1px'}}> Kabinet maakt publiekelijk excuses voor oude
                                Transgenderwet</h5>
                        </a>
                    </div>

                </Grid.Column>

                <Grid.Column floated='right' width={10}>
                    <div style={{padding: 0, margin: '1px 1px 1px -400px', width: '1300px'}}>
                        <Container centered fluid>
                            <Card centered fluid className="custom_card_article">
                                <Card.Content>
                                    <Header textAlign="center" className={title}>
                                        {article.title}
                                    </Header>
                                    <div>
                                        <Image className="img_desktop" centered src={image_id}/>
                                    </div>
                                    <Card.Content className={teaser}>{article.teaser}</Card.Content>
                                </Card.Content>
                                <Card.Content className={text}>
                                    {ReactHtmlParser(article.text)}
                                </Card.Content>
                            </Card>
                        </Container>
                        <Menu secondary borderless size="massive" fixed="bottom">
                            <MenuItem
                                className="article_menu"
                                name="Terug naar de Homepage"
                                position="right"
                                icon="home"
                                onClick={navigateToNewsfeed}
                            ></MenuItem>
                        </Menu>

                    </div>
                </Grid.Column>
            </Grid>
        </div>

    )
}
